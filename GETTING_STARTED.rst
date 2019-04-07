***************
Getting Started
***************

Our code is hosted here: https://github.com/codethechange/mobility_pipeline

=================================
Getting the Code and Dependencies
=================================

#. Choose where you want to download the code, and navigate to that directory.
   Then download the code.

    .. code-block:: console

      $ cd path/to/desired/directory
      $ git clone https://github.com/codethechange/mobility_pipeline.git

#. Install python 3 from https://python.org or via your favorite package manager

#. Install ``virtualenv``

    .. code-block:: console

      $ pip3 install virtualenv

#. If you get a note from ``pip`` about ``virtualenv`` not being in your
   ``PATH``, you need to perform this step. ``PATH`` is a variable accessible
   from any bash terminal you run, and it tells bash where to look for the
   commands you enter. It is a list of directories separated by ``:``. You can
   see yours by running ``echo $PATH``. To run ``virtualenv`` commands, you need
   to add python's packages to your ``PATH`` by editing or creating the file
   ``~/.bash_profile`` on MacOS. To that file add the following lines:

    .. code-block:: console

      PATH="<Path from pip message>:$PATH"
      export PATH

#. Then you can install dependencies into a virtual environment

    .. code-block:: console

      $ cd name_of_cloned_repository
      $ virtualenv -p python3 venv
      $ source venv/bin/activate
      $ pip install -r requirements.txt

Now you're all set!
