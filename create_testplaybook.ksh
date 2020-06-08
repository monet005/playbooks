#!/usr/bin/ksh

JIRA=$1

echo "Creating playbooks and requirements file"

cat >${JIRA}-requirements.yml <<EOF
---
- src: git+https://github.com/monet005/approle.git
  scm: git
  version: $JIRA
  name: approle
EOF

cat >${JIRA}.yml <<EOF
---
- include_role:
    name: approle
EOF

cat >base.yml <<EOF
---
- name: provisioning play
  hosts: localhost
  connection: local

  tasks:
    - name: download the requirements
      shell: |
        ansible-galaxy install --roles-path {{ playbook_dir }} -r "{{ playbook }}-requirements.yml"

    - name: "start {{ playbook }}"
      include_tasks: "{{ playbook }}.yml"
EOF

echo "Execute below ansible command:"
echo "ansible-playbook base.yml -e playbook=$JIRA"


