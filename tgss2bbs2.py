#!/usr/bin/env python
"""
tgss2bbs.py

This script sources from the TGSS VO server and creates a BBS compatible skymodel.

Written by Sarrvesh S. Sridhar.
Last updated: Sep 18 2016
Updated by Alexandar Mechev.
Deconvolution script by Joshua Albert
"""
from astropy.coordinates import get_icrs_coordinates
import pyvo as vo
import optparse
import radec_to_string #astropyless conversion of ra-dec co-ordinates
import math
import BeamDeconvolution as Beam_deconv_new #deconvolution of tgss beam

def main(srcID,radius,DoDec=True,output="tgss.skymodel"):
   """
   tgss2bbs2: 
   
   This inputs are srcID (string) as a co-ordinate or object ID
                   radius (float) is radius in degrees, converted in caller function
                   DoDec (bool) Option to do deconvolution
   The result is saved in atext file which is both logged locally and sent to the user
        through wget or through the browser
   """
   patch=True

   objName = srcID
   radInDeg = float(radius)
   outFileName = output
   inOnePatch = patch

   # Get the sources in the cut-out as a VO table 
   url = 'http://vo.astron.nl/tgssadr/q/cone/scs.xml'
   try:
      t = vo.conesearch(url, pos = get_icrs_coordinates(objName), radius = radInDeg )
   except IndexError:
      f=open(outFileName,'w')
      f.write("Index Error when polling VirtualObservatory. Bad object name??")
      f.close()
      return

   f = open(outFileName, 'w')
   if patch:
      # Write all selected components as a single patch
      f.write("FORMAT = Name, Type, Patch, Ra, Dec, I, Q, U, V, MajorAxis, MinorAxis, Orientation, ReferenceFrequency='147500000.0', SpectralIndex='[]'\n\n")
      # Get the coordinates of the source
      c=radec_to_string.radec_to_string([get_icrs_coordinates(objName).ra.value,get_icrs_coordinates(objName).dec.value],separators = [ ':', ':', '$', '.', ".", '' ])
      newRA = c.split("$")[0]
      newDec = c.split("$")[1]
      # Create the header
      f.write(' , , Patch, {ra}, {dec}\n'.format(ra=newRA, dec=newDec))

      for item in t:
        # VO table has RA and DEC in degrees. Convert it to hmsdms format
         coords=radec_to_string.radec_to_string([float(item['RA']),float(item['DEC'])],separators = [ ':', ':', '$', '.', ".", '' ])
         newRA = coords.split("$")[0]
         newDec = coords.split("$")[1]
         #use radec_to_string to convert coordinates instead of Astropy
         if ((item['Sint']/item['Spk'])>(2*math.sqrt(0.027**2+(0.784*(item['Spk']/item['Island_RMS'])**(-0.925))**2)+1.071)):
            srctp='GAUSSIAN'
            if not DoDec:
                maja=item['MAJAX']
                mina=item['MINAX']
                pax=item['PA']

            else:
                bmaj1,bmin1,bpa1=Beam_deconv_new.psfTGSS1(item["DEC"])
                A1,B1,C1 = Beam_deconv_new.elliptic2quadratic(bmaj1,bmin1,bpa1)
                A2,B2,C2 = Beam_deconv_new.elliptic2quadratic(item["MAJAX"],item["MINAX"],item["PA"])
                Ak,Bk,Ck = Beam_deconv_new.deconvolve(A2,B2,C2,A1,B1,C1)
                maja,mina,pax= Beam_deconv_new.quadratic2elliptic(Ak,Bk,Ck)
                if maja==None:
                    maja=""
                    mina=""
                    pax=""
                else:
                ## Some nice pretty formatting
                    maja="{0:0.1f}".format(maja)
                    mina="{0:0.1f}".format(mina)
                    pax="{0:0.1f}".format(pax)
            if pax<10 and pax!="":
                pa1="{0:.2f}".format(float(pax))
            else:
                pa1=pax
            if item['PA']>0:
                paxi=' '+str(pa1)
            else:
                paxi=pa1
            if pax=='' or pax=='nan': #Deconvolution fails to converge. Made it into a point source for now
                srctp='POINT   '
                maja='    '
                mina='    '
                paxi='     '
         else:
            srctp='POINT   '
            maja='    '
            mina='    '
            paxi='     '


        # Write an entry for this source into the output file inside the above defined patch
         f.write("{name}, {src}, Patch, {ra}, {dec}, {i}, 0, 0, 0, {ma}, {mi}, {pa}, , [-0.73]\n".format(name=item['ID'], src=srctp,ra=newRA, dec=newDec, i='{0: >9}'.format(format(item['Sint']/1e3,'.4f')), ma=maja, mi=mina, pa=paxi))
   else:
      # Writes sources without a patch
      f.write("FORMAT = Name, Type, Ra, Dec, I, Q, U, V, MajorAxis, MinorAxis, Orientation, ReferenceFrequency='147610000.0', SpectralIndex='[]'\n\n")
      for item in t:
        # VO table has RA and DEC in degrees. Convert it to hmsdms format
        coords=radec_to_string.radec_to_string([float(item['RA']),float(item['DEC'])],separators = [ ':', ':', '$', '.', ".", '' ])
        newRA = coords.split("$")[0]
        newDec = coords.split("$")[1]
        # Write an entry for this source into the output file
         #Case Gaussian
        f.write("{name}, GAUSSIAN, {ra}, {dec}, {i}, 0, 0, 0, {ma}, {mi}, {pa}, , [-0.8]\n".format(name=item['ID'], ra=newRA, dec=newDec, i=item['Sint']/1e3, ma=item['MAJAX'], mi=item['MINAX'], pa=item['PA']))
   f.close()

if __name__ == '__main__':
   """creates a skymodel from commandline arguments. 
   """
   opt = optparse.OptionParser()
   opt.add_option('-s', '--srcID', help='Resolveable source name [no default]', default='')
   opt.add_option('-r', '--radius', help='Search radius in deg [default: 5.0 deg]', default='5.0')
   opt.add_option('-o', '--output', help='Output filename [default: tgss.skymodel]', default='tgss.skymodel')
   opt.add_option('-p', '--patch', help='Write all sources as a single patch? [default: True]', action='store_true')
   opt.add_option('-d', '--dodec',help='Deconvolve the TGSS Beam [default: True]',default=True)
   options, arguments = opt.parse_args()
   
   if options.srcID == '':
      raise Exception('Error: A valid source name must be given.')

   main(options.srcID,options.radius,options.dodec,options.output)
