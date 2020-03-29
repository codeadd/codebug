FROM archlinux

# Install Python 3, PyQt5
RUN pacman --noconfirm -Syu \
      && pacman --noconfirm -S mesa libgl vlc \
      && pacman --noconfirm -S python-setuptools \
      python-pip \
      python-qscintilla-qt5 \
      python-ply \
      python-networkx \
      python-numpy \
      python-matplotlib

# RUN python3 -V
# RUN pip3 freeze
