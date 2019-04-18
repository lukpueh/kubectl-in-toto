#!/usr/bin/env python3

import in_toto.models.layout as l
import in_toto.models.metadata as m
import in_toto.util as util


# keys = util.import_gpg_public_keys_from_keyring_as_dict(['functionary.pub'])
project_owner = util.import_rsa_key_from_file('project-owner')

layout = l.Layout()
keyid = layout.add_functionary_key_from_path('functionary.pub')['keyid']

step = l.Step()
step.name = 'build'
step.expected_products = [['REQUIRE', 'image_id']]
step.set_expected_command_from_string(
    'docker build . -t empty --idfile image_id')
step.pubkeys = [keyid]

inspection = l.Inspection()
inspection.name = 'verify-image'
inspection.expected_materials = [
    ['REQUIRE', 'image_id'],
    ['MATCH', 'image_id', 'WITH', 'PRODUCTS', 'FROM', 'build'],
    ['DISALLOW', '*']
  ]
inspection.set_run_from_string('echo lol')

layout.steps.append(step)
layout.inspect.append(inspection)

metablock = m.Metablock(signed=layout)
metablock.sign(project_owner)
metablock.dump("root.layout")
