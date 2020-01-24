from subprocess import call
from parameters import xml_str, xml_str_sim, xml_str_cell, xml_str_network, xml_str_conf
import xml.dom.minidom as md
import os
import numpy
import shutil as sh
from distutils.dir_util import copy_tree


def createFolder(directory):
	try:
		if not os.path.exists(directory):
			os.makedirs(directory)
	except OSError:
		print("Error creating directory.")


# Number of parameter files will be generated
# tnf_concentration [0.1,0.5] step 0.1
for tnf_conc in numpy.arange(0.1, 0.5, 0.1):
	# Create folder where to put the xml file
	#example_dir = createFolder('./example_spheroid_TNF_pulse0-600_conc%s' %(tnf_conc))
	# Initialize run's id
	i = 0;
	# time_add_tnf [0,600] step 25
	for tnf_time in range(25, 625, 25):
		#current_path = os.getcwd()
		#print("The current working directory is: %s" % current_path)
		
		# Create run folder
		run_dir = createFolder("./example_spheroid_TNF_conc%.1f_pulse0-600/run%s" %(tnf_conc,i))
		sh.copy2('./init.txt', './example_spheroid_TNF_conc%.1f_pulse0-600/run%s' %(tnf_conc,i))

		# Each run folder should contain 2 output subfolders: output, microutput
		output_dir = createFolder('./example_spheroid_TNF_conc%.1f_pulse0-600/run%s/output' %(tnf_conc,i))		
		microutput_dir = createFolder('./example_spheroid_TNF_conc%.1f_pulse0-600/run%s/microutput' %(tnf_conc,i))			

		# Call the file that creates the desirable xml file
		call(["python", "parameters.py"])

		# The name of the document
		xml_filename = ("./example_spheroid_TNF_conc%.1f_pulse0-600/run%s/parameters.xml" %(tnf_conc,i))

		# Write the generated xml file
		with open(xml_filename, "w") as f:
			f.write(xml_str)				#xml_str: the xml file as a string

		f.close()	

		# The XML file has been generated	


		# ------------------------- Change values for parameters ------------------------- #	

		# Import data by reading the file that just created

		# For simulation root
		sim_root = md.parseString(xml_str_sim)
		# Update the desirable values
		output_interval_element = sim_root.getElementsByTagName('output_interval')
		# update the text - value
		output_interval_element[0].firstChild.nodeValue = str(40)
		# Updated XML file as string
		tmp_updated_xml_str_sim = sim_root.toxml() + "\n"
		updated_xml_str_sim = tmp_updated_xml_str_sim[0:22] + "\n" + tmp_updated_xml_str_sim[22:116] + "\n" + tmp_updated_xml_str_sim[116:]


		# For cell_properties root
		cell_root = md.parseString(xml_str_cell)
		# update the text - value
		tmp_updated_xml_str_cell = cell_root.toxml() + "\n"
		updated_xml_str_cell = "\n" + tmp_updated_xml_str_cell[22:98] + "\n" + tmp_updated_xml_str_cell[98:]


		# For network root
		# network_root = md.parseString(xml_str_network)
		# Update the desirable values


		# For initial configuration root
		initial_conf_root = md.parseString(xml_str_conf)
		# Update values
		tnf_concentration_element = initial_conf_root.getElementsByTagName('tnf_concentration')
		# update the text - value
		tnf_concentration_element[0].firstChild.nodeValue = round(tnf_conc,1)	# desirable tnf window
		#duration_add_tnf_element[0].firstChild.nodeValue = tnf_window
		time_add_tnf_element = initial_conf_root.getElementsByTagName('time_add_tnf')
		time_add_tnf_element[0].firstChild.nodeValue = tnf_time		#desirable tnf pulse
		#duration_add_tnf_element = initial_conf_root.getElementsByTagName('duration_add_tnf')
		#duration_add_tnf_element[0].firstChild.nodeValue = str(10)

		# Updated XML file as string
		tmp_updated_xml_str_initial_conf = initial_conf_root.toprettyxml() + "\n"
		updated_xml_str_initial_conf = tmp_updated_xml_str_initial_conf[22:]


		updated_xml_str = updated_xml_str_sim + updated_xml_str_cell + xml_str_network + updated_xml_str_initial_conf

		with open(xml_filename, "w") as f:
			f.write(updated_xml_str)

		f.close()
		i += 1

	bn_dir = createFolder("./example_spheroid_TNF_conc%.1f_pulse0-600/BN" %tnf_conc)
	copy_tree('./BN', './example_spheroid_TNF_conc%.1f_pulse0-600/BN' %tnf_conc)