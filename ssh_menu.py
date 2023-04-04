from pick import pick
import yaml
import subprocess

yamldocs = []

with open('hosts.yml', 'r') as file:
    docs = yaml.safe_load_all(file)
    for doc in docs:
        yamldocs.append(doc)

host_list = yamldocs[0]
defaults = yamldocs[1]['Defaults']

####
#### Select Host category
####

categories = []
for key in host_list.items():
  categories.append(key[0])

title = "Please pick a category"
category = pick(categories, title)

###
### Select Site
###

sites = []
for s in host_list[category[0]].items():
   sites.append(s[0])

title = "Please pick a site"
site = pick(sites, title)


###
### Select a host
###

hlist = []
for hostname,username in host_list[category[0]][site[0]].items():
  hlist.append(hostname)

title = "Please pick a host"
host = pick(hlist, title)

hn = host[0]


###
### Check host options
###

parameters = ["ssh"]
host_object = host_list[category[0]][site[0]][host[0]]

if host_object:
  if 'username' in host_object:
    if not host_object['username'] == "" and not host_object['username'] == None:
      un = host_object['username']
      parameters.append("-l")
      parameters.append(un)
else:
  if 'username' in defaults:
    if not defaults['username'] == "" and not defaults['username'] == None:
      un = defaults['username']
      parameters.append("-l")
      parameters.append(un)

  # x11 forwarding
if host_object:
  if 'xforward' in host_object:
     if host_object['xforward'] == True:
        parameters.append("-X")

  # port forwarding
if host_object:
  if 'port_forward' in host_object:
    pf = host_object['port_forward']
    
    
    # local port forwarding
    pf_local = host_object['port_forward']['local']
    if 'local' in pf:
      if 'local_port' in pf_local:
        if type(pf_local['local_port']) == int:
          l_local_port = pf_local['local_port']

      if 'remote_port' in pf_local:
        if type(pf_local['remote_port']) == int:
          l_remote_port = pf_local['remote_port']

      if 'destination_server' in pf_local:
        if type(pf_local['destination_server']) == str:
          destination_server = pf_local['destination_server']

      if 'l_local_port' in locals() and 'l_remote_port' in locals() and 'destination_server' in locals():
        parameters.append('-L')
        parameters.append(f"{l_local_port}:{destination_server}:{l_remote_port}")

    # remote port forwarding
    pf_remote = host_object['port_forward']['remote']


    if 'remote' in pf:
      if 'local_port' in pf_remote:
        if type(pf_remote['local_port']) == int:
          r_local_port = pf_remote['local_port']
      if 'remote_port' in pf_remote:
        if type(pf_remote['remote_port']) == int:
          r_remote_port = pf_remote['remote_port']
      if 'r_local_port' in locals() and 'r_remote_port' in locals():
        parameters.append('-R')
        parameters.append(f"{r_local_port}:localhost:{r_remote_port}")

    # dynamic port forwarding
    pf_dyn = host_object['port_forward']['dynamic']

    if 'dynamic' in pf_dyn:
      if 'port' in pf_dyn:
        if type(pf_dyn['port']) == int:
          d_port = pf_dyn['port']
      if 'd_port' in locals():
        parameters.append('-D')
        parameters.append(f"{d_port}")

  #arbitrary options
if host_object:
  if 'options' in host_object:
     if not host_object['options'] == "" and not host_object['options'] == None:
      options_strings = (host_object['options']).split(' ')
      for option in options_strings:
        parameters.append(option)

parameters.append(host[0])


###
### Connect to host with options
###

print(parameters)
subprocess.run(parameters)