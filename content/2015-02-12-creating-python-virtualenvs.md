Title: Creating python virtual environments
Tags: python, agile
Status: published
Date: 2015-02-12 13:41:31

Using **virtualenv** while working on python projects helps in many ways:

- Minimizes the risk of bad dependencies between different projects under
development in the same machine
- Minimizes the risk of bad dependencies amongst members of the same team
- Allows a fast and easy sandbox for testing small chunks of code, new
libraries, etc without affecting other projects
- Allows working with different python versions (major and minor)

A convenient way to set it up is using
[`virtualenvwrapper`](http://virtualenvwrapper.readthedocs.org/en/latest/index.html)
(assuming everything's in place and shell startup file was sourced and
`WORKON_HOME` is set to `/data/venv`):

    :::console
    $ mkvirtualenv test_project
    (test_project) /data/venv/test_project $ pip install django
    (test_project) /data/venv/test_project $ python --version
    Python 3.5.0
    (test_project) /data/venv/test_project $ deactivate

    # Create a python2 virtualenv
    /data/venv/test_project $ cd
    ~ $ mkvirtualenv tests_py2 --python=`which python2`

    # populate the third party libraries from a requirements file
    (tests_py2) /data/venv/tests_py2 $ cd /devel
    (tests_py2) /devel $ pip install -r requirements.txt
    (tests_py2) /devel $ cd  #go back to the virtualenv's home folder
    (tests_py2) /data/venv/tests_py2 $ python --version
    Python 2.7.10


If using `ipython` as the interactive python interpreter, we can set a
`postactivate` hook in `$WORKON_HOME` to load the correct version of
`ipython`:

    :::zsh hl_lines="12"
    #!/usr/bin/zsh
    # This hook is sourced after every virtualenv is activated.
    cd () {
        if (( $# == 0 ))
        then
            builtin cd $VIRTUAL_ENV/$(basename $VIRTUAL_ENV)
        else
            builtin cd "$@"
        fi
    }
    cd
    if [[ $(python --version 2>&1) == *2* ]]; then alias ipython=/usr/bin/ipython2; else alias ipython=/usr/bin/ipython3; fi

Plus the next snippet for running `ipython` inside virtual environments (under
`~/.ipython/profile_default/startup/`, for example `50-run-inside-venv.py`) as
explained [here](http://igotgenes.blogspot.com.es/2010/01/interactive-sandboxes-using-ipython.html):

    :::python
    from __future__ import print_function
    
    import site
    import sys
    from os import environ
    from os.path import join
    
    if 'VIRTUAL_ENV' in environ:
        virtual_env = join(environ.get('VIRTUAL_ENV'),
                           'lib',
                           'python%d.%d' % sys.version_info[:2],
                           'site-packages')
    
        # Remember original sys.path.
        prev_sys_path = list(sys.path)
        site.addsitedir(virtual_env)
    
        # Reorder sys.path so new directories at the front.
        new_sys_path = []
        for item in list(sys.path):
            if item not in prev_sys_path:
                new_sys_path.append(item)
                sys.path.remove(item)
        sys.path[1:1] = new_sys_path
    
        print('virtualenv->', virtual_env)
        del virtual_env
    
    del site, environ, join, sys


##Update

If we have the <u>**powerline extension**</u> for `ipython`, we can invoke it
directly before entering the virtualenv.
With the scenario described above this is as ease as adding these lines to
ipython's configuration file `~/.ipython/profile_default/ipython_config.py`:

    :::python
    if not hasattr(sys, 'real_prefix'):  # Running outside a virtualenv
        c.InteractiveShellApp.extensions = [
           'powerline.bindings.ipython.post_0_11'
       ]

In case we decide to install ipython **inside** the virtualenv, the previous
code will skip not use the powerline extension while within the virtualenv.
This is usually the right thing because otherwise we should install
`powerline-status in all our virtual environments.

## Update (II)

If using ST3 as text editor it may be convenient to add the following hook to
`postmkvirtualenv`:

    :::zsh hl_lines="4"
    #!/usr/bin/zsh
    # This hook is sourced after a new virtualenv is activated.
    proj_name=$(basename $VIRTUAL_ENV)
    sed 's\$VIRTUAL_ENV\'$VIRTUAL_ENV'\g' $WORKON_HOME/skeleton.sublime-project >> $VIRTUAL_ENV/$proj_name.sublime-project
    add2virtualenv $VIRTUAL_ENV/$proj_name

so the template file (`skeleton.sublime-project`, see below) is copied with
the appropriate name inside the newly created virtual environment.

    :::json hl_lines="8 20"   
    {
            "build_systems":
            [
                    {
                            "file_regex": "^[ ]*File \"(...*?)\", line ([0-9]*)",
                            "name": "Anaconda Python Builder",
                            "selector": "source.python",
                            "shell_cmd": "$VIRTUAL_ENV/bin/python -u \"$file\""
                    }
            ],
            "folders":
            [
                    {
                "follow_symlinks": true,
                            "path": "."
                    }
            ],
            "settings":
            {
                    "python_interpreter": "$VIRTUAL_ENV/bin/python"
            }
    }

For reference, other customized hook scripts:

- `premkvirtualenv`

        :::bash
        mkdir -p $WORKON_HOME/$1/$1

- `postdeactivate`

        :::bash
        cd $WORKON_HOME
