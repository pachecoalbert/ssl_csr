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
#parser.add_argument('stacktype', help='The stack type.',choices=["app","web","rds","sg","iam","batch","pub"])
#parser.add_argument('appFolder', help='The app folder where stack Metedata yaml file exists (appstack.yaml).')
#parser.add_argument('region', help='The region where the instance resides.')
#parser.add_argument('-p','--profile', help='The profile to be used.')
#parser.add_argument('-a','--AMIid', help='Used for RECOVERY only: The AMI ID that needs to be backed up.')
#parser.add_argument('-i','--InstanceID', help='Used for BACKUP only: The instance ID that needs to be backed up.')

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

print('cmd = ', cmd)

#subprocess.Popen(cmd,shell=True,cwd="/Users/pacheco/PycharmProjects/ssl_csr/bin")

subprocess.call(cmd,shell=True)
#output = subprocess.Popen(["cmd"], stdout=subprocess.PIPE).communicate()[0]


#subprocess.check_output(cmd,stderr=subprocess.STDOUT)

# EG openssl req -new -sha256 -newkey rsa:2048 -nodes -keyout sis.ws.dev.ats.cloud.huit.harvard.edu.key -out sis.ws.dev.ats.cloud.huit.harvard.edu.csr -subj "/C={}/ST=MA/L=Cambridge/O=Harvard University/OU=HUIT/CN=sis.ws.dev.ats.cloud.huit.harvard.edu"
exit(0)