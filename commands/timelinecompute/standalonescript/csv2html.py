#!/usr/bin/env python3
# (C) 2017 OpenEye Scientific Software Inc. All rights reserved.
#
# TERMS FOR USE OF SAMPLE CODE The software below ("Sample Code") is
# provided to current licensees or subscribers of OpenEye products or
# SaaS offerings (each a "Customer").
# Customer is hereby permitted to use, copy, and modify the Sample Code,
# subject to these terms. OpenEye claims no rights to Customer's
# modifications. Modification of Sample Code is at Customer's sole and
# exclusive risk. Sample Code may require Customer to have a then
# current license or subscription to the applicable OpenEye offering.
# THE SAMPLE CODE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED.  OPENEYE DISCLAIMS ALL WARRANTIES, INCLUDING, BUT
# NOT LIMITED TO, WARRANTIES OF MERCHANTABILITY, FITNESS FOR A
# PARTICULAR PURPOSE AND NONINFRINGEMENT. In no event shall OpenEye be
# liable for any damages or liability in connection with the Sample Code
# or its use.

#############################################################################
# Converts a CSV or a SDF file into HTML
#############################################################################

import sys
from openeye import oechem
from openeye import oedepict


def main(argv=[__name__]):

    itf = oechem.OEInterface(InterfaceData)
    oedepict.OEConfigure2DMolDisplayOptions(itf, oedepict.OE2DMolDisplaySetup_AromaticStyle)

    if not oechem.OEParseCommandLine(itf, argv):
        return 1

    iname = itf.GetString("-in")
    oname = itf.GetString("-out")

    # check input/output files

    ifs = oechem.oemolistream()
    if not ifs.open(iname):
        oechem.OEThrow.Fatal("Cannot open input file!")

    if ifs.GetFormat() not in [oechem.OEFormat_CSV, oechem.OEFormat_SDF]:
        oechem.OEThrow.Fatal("Input must be CSV or SDF file!")

    ext = oechem.OEGetFileExtension(oname)
    if ext != "html":
        oechem.OEThrow.Fatal("Output must be HTML format.")

    ofp = open(oname, "w")

    # import molecules

    mollist = []
    for mol in ifs.GetOEGraphMols():
        mollist.append(oechem.OEGraphMol(mol))

    # setup depiction options

    width, height = 200, 200
    opts = oedepict.OE2DMolDisplayOptions(width, height, oedepict.OEScale_AutoScale)
    oedepict.OESetup2DMolDisplayOptions(opts, itf)

    # collect data tags

    tags = CollectDataTags(mollist)

    # generate html file

    WriteHTMLFile(ofp, mollist, iname, tags, opts)

    return 0


def CollectDataTags(mollist):

    tags = []
    for mol in mollist:
        for dp in oechem.OEGetSDDataIter(mol):
            if not dp.GetTag() in tags:
                tags.append(dp.GetTag())

    return tags


def WriteHTMLFile(ofp, mollist, iname, tags, opts):

    WriteHTMLHeader(ofp, iname, tags)

    for mol in mollist:
        WriteHTMLTableRow(ofp, mol, opts, tags)

    WriteHTMLFooter(ofp)


def WriteHTMLTableRow(ofp, mol, opts, tags):

    ofp.write("<tr class=row>\n")

    # add image

    ofp.write("<td> %s \n </td>\n" % GetSVGImage(mol, opts))

    # write data

    for tag in tags:
        value = "N/A"
        if oechem.OEHasSDData(mol, tag):
            value = oechem.OEGetSDData(mol, tag)
        ofp.write("<td> %s </td>" % value)

    ofp.write("</tr>\n")


def GetSVGImage(mol, opts):

    oedepict.OEPrepareDepiction(mol)
    disp = oedepict.OE2DMolDisplay(mol, opts)
    imagestr = oedepict.OERenderMoleculeToString("bsvg", disp, False)
    return imagestr.decode("utf-8")


def WriteHTMLHeader(ofp, filename, tags):

    tablewidth = min(1800, (len(tags) + 1) * 200)

    ofp.write("<style type='text/css'>\n")
    ofp.write("h1                          "
              "{ text-align:center; border-width:thick; border-style:double;"
              "border-color:#BCC; }\n")
    ofp.write("table.csv                   "
              "{ border-spacing:1; background: #FFF; width:%dpx; }\n" % tablewidth)
    ofp.write("table.csv td, th            "
              "{ width:100px; text-align:center; padding:3px 3px 3px 3px; }\n")
    ofp.write("table.csv th                { height:50px; color:#FFF; background:#788; }\n")
    ofp.write("table.csv tr:nth-child(even){ color:#000; background:#FFE; }\n")
    ofp.write("table.csv tr:nth-child(odd) { color:#000; background:#FEF; }\n")
    ofp.write("table.csv tr:hover          { color:#000; background:#DDD; }\n")
    ofp.write("</style>\n")

    ofp.write("<html><h1>%s</h1>\n" % filename)

    ofp.write("<body>\n")
    ofp.write("<table class=csv>\n")
    ofp.write("<tbody>\n")

    ofp.write("<tr>\n")
    ofp.write("<th> Molecule</th>")

    # write data tags in table header

    for tag in tags:
        ofp.write("<th> %s </th>" % tag)
    ofp.write("\n</tr>\n")


def WriteHTMLFooter(ofp):

    ofp.write("</table>\n</body>\n</html>\n")


InterfaceData = '''
!CATEGORY "input/output options"

    !PARAMETER -in
      !ALIAS -i
      !TYPE string
      !REQUIRED true
      !KEYLESS 1
      !VISIBILITY simple
      !BRIEF Input filename(s)
    !END

    !PARAMETER -out
      !ALIAS -o
      !TYPE string
      !REQUIRED true
      !KEYLESS 2
      !VISIBILITY simple
      !BRIEF Output HTML filename (extension .html)
    !END

!END
'''

if __name__ == "__main__":
    sys.exit(main(sys.argv))
