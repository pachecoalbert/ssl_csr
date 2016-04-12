# -----------------------------------------------------------------------------
# - HEAD
# -----------------------------------------------------------------------------
import yaml
import argparse
import subprocess


# -----------------------------------------------------------------------------
# - METHODS
# -----------------------------------------------------------------------------

'''
This function will check if a '/' is at the end of
file path.  If it's not there then it will add it.
'''
def validate_file_path(file_path):

    # Grab the last character from the string
    last_char = file_path[-1]
    if last_char != '/':
        file_path += '/'
    return file_path

# -----------------------------------------------------------------------------
# - MAIN
# -----------------------------------------------------------------------------

'''
Use argpars to define the valid script arguements.
'''
parser = argparse.ArgumentParser(description="Utility to create CSR for SSL certs.")
parser.add_argument('csr_config', help='The config file used to create the csr and key files.')
parser.add_argument('file_output', help='The location to create the csr and key files.')

args = parser.parse_args()

'''
The location where the csr and key files will be created.
'''
output_dir = validate_file_path(args.file_output)

'''
Open the csr cofig file and load it into a dict.
'''
stream = open(args.csr_config, 'r')
# use safe_load instead load
csrMap = yaml.safe_load(stream)
stream.close()
#print csrMap

csr_subj = csrMap['csr_subj']
#print('csr_subj = ', csr_subj)

'''
Build the openssl command line call.
'''
cmd = "openssl req -new -sha256 -newkey rsa:2048 -nodes -keyout {0}{1}.key -out {0}{1}.csr -subj \"/C={2}/ST={3}/L={4}/O={5}/OU={6}/CN={1}\"\n".format(output_dir,csr_subj['common_name'],csr_subj['country'],csr_subj['state'],csr_subj['locality'],csr_subj['organization'],csr_subj['organization_unit'])

#print('cmd = ', cmd)

'''
Make a shell call to run the openssl command
'''
subprocess.call(cmd,shell=True)

exit(0)