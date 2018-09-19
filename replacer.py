#!/usr/bin/env python


import os
import sys
import getopt
from shutil import copyfile

class Usage(Exception):
  def __init__(self, msg):
    self.msg = msg

def main(argv=None):
  if argv is None:
    argv = sys.argv
  try:
    try:
      opts, args = getopt.getopt(argv[1:], "i:k:t:h", ["input=", "keys=", "type=", "help"])
    except msg:
      raise Usage(msg)
    # more code, unchanged
  except (Usage, err) as err:
    print >>sys.stderr, err.msg
    print >>sys.stderr, "for help use --help"
    return 2

  inputFile = ""
  allowedKeys = {}
  config = {}

  for o, a in opts:
    if o in ('-i', '--input'):
      inputFile = a
    elif o in ('-k', '--keys'):
      allowedKeys = set(a.split(','))
    elif o in ('-t', '--type'):
      if a == 'ansible':
        config = {
          "separator": ":",
          "replace_separator": ": "
        }
      else:
        config = {
          "separator": "=",
          "replace_separator": "="
        }
    elif o in ('-h', '--help'):
      print("the script takes environment variables as input, filters only allowed ones and then replaces values in specified configuration file")
      print("")
      print("replacer.py -i <input_file> -k <comma-separated_key_names_to_filter> -t <ansible|shell>")
      sys.exit()

  if not inputFile:
    raise Usage("Input file is missing. For help use -h or --help")
  if not allowedKeys:
    raise Usage("Allowed keys are missing. For help use -h or --help")

#  allowedKeys = { "ye_app_guide_server_version", "ye_app_logger_server_version", "ye_app_client_version", "ye_app_docs_version" }
  replaceDict = {k: v for k, v in os.environ.items() if k in allowedKeys}

  print("Config {}".format(config))
  print("Replacement dictionary:")
  print(str(replaceDict))

  result = ''

  copyfile(inputFile, inputFile + '.bak')

  with open(inputFile) as f:
    for line in f:
      if config['separator'] in line and '#' not in line:
        splitted = line.split(config['separator'])
        stripped = splitted[0].strip()
        if stripped in replaceDict and replaceDict[stripped]:
          print("replacing line", line)
          result += splitted[0] + config['replace_separator'] + replaceDict[stripped] + '\n'
        else:
          result += line
      else:
        result += line

  #print result

  fout = open(inputFile, 'w')
  fout.write(result)
  fout.close()

if __name__ == "__main__":
  sys.exit(main())

