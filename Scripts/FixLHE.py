import os, sys
import xml.etree.ElementTree as ET
'''
This script will add protons and fix mother idx of hard process particles
'''

#Global variables
BEAMENERGY  = 6500.0        # beam energy [GeV]
PROTON_MASS = 0.93827       # proton mass [GeV]

if (len(sys.argv) < 2):
    print('ERROR: missing input file\nUsage: python '+sys.argv[0]+' LHEFILE')
    sys.exit(0)

inFile=sys.argv[1]

if not os.path.exists(inFile):
  print('Cannot find'+inFile)
  sys.exit(0)

pp = ['     2212   -1    0    0    0    0   %0.8e   %0.8e   %0.8e   %0.8e   %0.8e 0. 9.'%(0.,0.,BEAMENERGY,BEAMENERGY,PROTON_MASS),
     '     2212   -1    0    0    0    0   %0.8e   %0.8e  -%0.8e   %0.8e   %0.8e 0. 9.'%(0.,0.,BEAMENERGY,BEAMENERGY,PROTON_MASS)]
# read lhe file
tree = ET.parse(inFile)
root=tree.getroot()

#loop over all events
for child in root:
  if(child.tag=='event'):
    text=child.text
    lines=text.split('\n')
    
    #update number of particles
    event_header=lines[1]
    N=int(event_header.split()[0].strip())
    lines[1]=event_header.replace('     '+str(N),'     '+str(N+2))

    #add two incomming protons
    lines.insert(2,pp[0])
    lines.insert(3,pp[1])

    #set mothers to outgoing particles
    for i, l in enumerate(lines[6:-1]):
      lines[i+6]=l.replace('    0    0    0    0','    1    2    0    0')

    #write updated event
    child.text='\n'.join(lines)

#save fixed file
tree.write(inFile.replace('.lhe','_fix.lhe'))
