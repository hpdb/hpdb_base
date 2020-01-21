#!/usr/bin/env bash
set -e
rootdir=$( cd $(dirname $0) ; pwd -P )
exec >  >(tee install.log)
exec 2>&1

cd $rootdir
mkdir -p bin
mkdir -p thirdParty
cd thirdParty

export PATH=$PATH:$rootdir/bin:$rootdir/thirdParty/Anaconda2/bin

alignments_tools=( clustalo snippy mafft kma muscle mummer )
analysis_tools=( roary )
annotation_tools=( BLAST+ blastall phage_finder aragorn prodigal prokka tRNAscan )
classification_tools=( centrifuge )
phylogeny_tools=( phylip )
utility_tools=( Anaconda2 JBrowse circos )
all_tools=( "${alignments_tools[@]}" "${analysis_tools[@]}" "${annotation_tools[@]}" "${classification_tools[@]}" "${phylogeny_tools[@]}" "${utility_tools[@]}" )

install_Anaconda2() {
  echo "------------------------------------------------------------------------------
                          Installing Anaconda2
  ------------------------------------------------------------------------------
  "
  if [ ! -f $rootdir/thirdParty/Anaconda2/bin/python ]; then
    wget -c https://repo.anaconda.com/archive/Anaconda2-2019.10-Linux-x86_64.sh
    bash Anaconda2-2019.10-Linux-x86_64.sh -b -p $rootdir/thirdParty/Anaconda2/
  fi
  anacondabin=$rootdir/thirdParty/Anaconda2/bin/
  ln -fs $anacondabin/python $rootdir/bin
  ln -fs $anacondabin/pip $rootdir/bin
  ln -fs $anacondabin/conda $rootdir/bin
  $anacondabin/conda install -y biopython
  $anacondabin/pip install regex htmldom PyPDF2 mysqlclient
  #sed -i -E 's%/tmp/build/[a-zA-Z0-9]+/perl_[0-9]+/_build_env%/home/hpdb/base/thirdParty/Anaconda2%g' /home/hpdb/base/thirdParty/Anaconda2/lib/5.26.2/x86_64-linux-thread-multi/Config_heavy.pl
  #sed -i -E 's%/tmp/build/[a-zA-Z0-9]+/perl_[0-9]+/_build_env%/home/hpdb/base/thirdParty/Anaconda2%g' /home/hpdb/base/thirdParty/Anaconda2/lib/5.26.2/x86_64-linux-thread-multi/CORE/config.h
  #sed -i -E 's%/tmp/build/[a-zA-Z0-9]+/perl_[0-9]+/_build_env%/home/hpdb/base/thirdParty/Anaconda2%g' /home/hpdb/base/thirdParty/Anaconda2/lib/5.26.2/x86_64-linux-thread-multi/Config.pm
  echo "
  ------------------------------------------------------------------------------
                          Anaconda2 Installed
  ------------------------------------------------------------------------------
  "
}

install_BLAST+() {
  echo "------------------------------------------------------------------------------
                            Installing ncbi-blast-2.9.0+-x64
  ------------------------------------------------------------------------------
  "
  wget -c ftp://ftp.ncbi.nlm.nih.gov/blast/executables/blast+/2.9.0/ncbi-blast-2.9.0+-x64-linux.tar.gz
  tar -xzf ncbi-blast-2.9.0+-x64-linux.tar.gz
  cd ncbi-blast-2.9.0+
  cp -fR bin/* $rootdir/bin/.
  cd $rootdir/thirdParty
  echo "
  ------------------------------------------------------------------------------
                            ncbi-blast-2.9.0+-x64 installed
  ------------------------------------------------------------------------------
  "
}

install_blastall()
{
  echo "------------------------------------------------------------------------------
                            Install blast-2.2.26-x64-linux
  ------------------------------------------------------------------------------
  "
  wget -c ftp://ftp.ncbi.nlm.nih.gov/blast/executables/legacy.NOTSUPPORTED/2.2.26/blast-2.2.26-x64-linux.tar.gz
  tar -xzf blast-2.2.26-x64-linux.tar.gz
  cd blast-2.2.26
  cp -fR bin/* $rootdir/bin/.
  cd $rootdir/thirdParty
  echo "
  ------------------------------------------------------------------------------
                            blast-2.2.26-x64 installed
  ------------------------------------------------------------------------------
  "
}

install_aragorn()
{
  echo "------------------------------------------------------------------------------
                            Compiling aragorn1.2.38
  ------------------------------------------------------------------------------
  "
  wget -c http://130.235.244.92/ARAGORN/Downloads/aragorn1.2.38.tgz
  tar -xzf aragorn1.2.38.tgz
  cd aragorn1.2.38
  gcc -O3 -ffast-math -finline-functions -o aragorn aragorn1.2.38.c
  cp -fR aragorn $rootdir/bin/.
  cd $rootdir/thirdParty
  echo "
  ------------------------------------------------------------------------------
                            aragorn1.2.38 compiled
  ------------------------------------------------------------------------------
  "
}

install_prodigal() {
  echo "------------------------------------------------------------------------------
                            Installing prodigal v2.6.3
  ------------------------------------------------------------------------------
  "
  wget -c https://github.com/hyattpd/Prodigal/releases/download/v2.6.3/prodigal.linux -O prodigal-v2.6.3
  cp prodigal-v2.6.3 $rootdir/bin/prodigal
  chmod +x $rootdir/bin/prodigal
  cd $rootdir/thirdParty
  echo "
  ------------------------------------------------------------------------------
                            prodigal v2.6.0 installed
  ------------------------------------------------------------------------------
  "
}

install_prokka()
{
  echo "------------------------------------------------------------------------------
                            Installing prokka
  ------------------------------------------------------------------------------
  "
  #$rootdir/thirdParty/Anaconda2/bin/conda install -y -c bioconda prokka
  git clone https://github.com/tseemann/prokka.git prokka
  ln -fs `pwd`/prokka/bin/prokka $rootdir/bin
  echo "
  ------------------------------------------------------------------------------
                            prokka installed
  ------------------------------------------------------------------------------
  "
}

install_tRNAscan()
{
  echo "------------------------------------------------------------------------------
                            Installing tRNAscan-SE 2.0.4
  ------------------------------------------------------------------------------
  "
  wget -c http://trna.ucsc.edu/software/trnascan-se-2.0.4.tar.gz
  tar -xzf trnascan-se-2.0.4.tar.gz
  cd tRNAscan-SE-2.0
  ./configure --prefix=$rootdir && make && make install
  cd $rootdir/thirdParty
  echo "
  ------------------------------------------------------------------------------
                            tRNAscan-SE 2.0.4 installed
  ------------------------------------------------------------------------------
  "
}

install_clustalo() {
  echo "------------------------------------------------------------------------------
                            Installing Clustal Omega
  ------------------------------------------------------------------------------
  "
  wget -c http://www.clustal.org/omega/clustal-omega-1.2.4.tar.gz
  tar -xzf clustal-omega-1.2.4.tar.gz
  cd clustal-omega-1.2.4
  ./configure --prefix=$rootdir && make && make install
  cd $rootdir/thirdParty
  echo "------------------------------------------------------------------------------
                            Clustal Omega installed
  ------------------------------------------------------------------------------
  "
}

install_bcftools() {
  echo "------------------------------------------------------------------------------
                            Installing bcftools
  ------------------------------------------------------------------------------
  "
  wget -c https://github.com/samtools/bcftools/releases/download/1.9/bcftools-1.9.tar.bz2
  tar -xjf bcftools-1.9.tar.bz2
  cd bcftools-1.9
  ./configure --prefix=$rootdir && make && make install
  cd $rootdir/thirdParty
  echo "------------------------------------------------------------------------------
                            bcftools installed
  ------------------------------------------------------------------------------
  "
}

install_htslib() {
  echo "------------------------------------------------------------------------------
                            Installing htslib
  ------------------------------------------------------------------------------
  "
  wget -c https://github.com/samtools/htslib/releases/download/1.9/htslib-1.9.tar.bz2
  tar -xjf htslib-1.9.tar.bz2
  cd htslib-1.9
  ./configure --prefix=$rootdir && make && make install
  cd $rootdir/thirdParty
  echo "------------------------------------------------------------------------------
                            htslib installed
  ------------------------------------------------------------------------------
  "
}

install_samtools() {
  echo "------------------------------------------------------------------------------
                            Installing samtools
  ------------------------------------------------------------------------------
  "
  wget -c https://github.com/samtools/samtools/releases/download/1.9/samtools-1.9.tar.bz2
  tar -xjf samtools-1.9.tar.bz2
  cd samtools-1.9
  ./configure --prefix=$rootdir && make && make install
  cd $rootdir/thirdParty
  echo "------------------------------------------------------------------------------
                            samtools installed
  ------------------------------------------------------------------------------
  "
}

install_minimap2() {
  echo "------------------------------------------------------------------------------
                            Installing minimap2
  ------------------------------------------------------------------------------
  "
  wget -c https://github.com/lh3/minimap2/releases/download/v2.17/minimap2-2.17_x64-linux.tar.bz2
  tar -xjf minimap2-2.17_x64-linux.tar.bz2
  cp minimap2-2.17_x64-linux/minimap2 $rootdir/bin
  echo "------------------------------------------------------------------------------
                            minimap2 installed
  ------------------------------------------------------------------------------
  "
}

install_snpsites() {
  echo "------------------------------------------------------------------------------
                            Installing snp-sites
  ------------------------------------------------------------------------------
  "
  wget -c https://github.com/sanger-pathogens/snp-sites/archive/v2.5.1.tar.gz -O snp-sites-v2.5.1.tar.gz
  tar -xzf snp-sites-v2.5.1.tar.gz
  cd snp-sites-2.5.1
  autoreconf -i -f
  ./configure --prefix=$rootdir && make && make install
  cd $rootdir/thirdParty
  echo "------------------------------------------------------------------------------
                            snp-sites installed
  ------------------------------------------------------------------------------
  "
}

install_seqtk() {
  echo "------------------------------------------------------------------------------
                            Installing seqtk
  ------------------------------------------------------------------------------
  "
  git clone https://github.com/lh3/seqtk.git;
  cd seqtk; make
  cp seqtk $rootdir/bin
  cd $rootdir/thirdParty
  echo "------------------------------------------------------------------------------
                            seqtk installed
  ------------------------------------------------------------------------------
  "
}

install_vt() {
  echo "------------------------------------------------------------------------------
                            Installing vt
  ------------------------------------------------------------------------------
  "
  git clone https://github.com/atks/vt
  cd vt; make
  cp vt $rootdir/bin
  cd $rootdir/thirdParty
  echo "------------------------------------------------------------------------------
                            vt installed
  ------------------------------------------------------------------------------
  "
}

install_freebayes() {
  echo "------------------------------------------------------------------------------
                            Installing freebayes
  ------------------------------------------------------------------------------
  "
  wget -c https://github.com/ekg/freebayes/releases/download/v1.3.1/freebayes-v1.3.1
  cp freebayes-v1.3.1 $rootdir/bin/freebayes
  chmod +x $rootdir/bin/freebayes
  echo "------------------------------------------------------------------------------
                            freebayes installed
  ------------------------------------------------------------------------------
  "
}

install_snippy() {
  echo "------------------------------------------------------------------------------
                            Installing snippy
  ------------------------------------------------------------------------------
  "
  install_bcftools
  install_htslib
  install_samtools
  install_minimap2
  install_snpsites
  install_seqtk
  install_vt
  install_freebayes
  wget -c https://github.com/tseemann/snippy/archive/v4.4.3.tar.gz -O snippy-4.4.3.tar.gz
  tar -xzf snippy-4.4.3.tar.gz
  ln -fs `pwd`/snippy-4.4.3/bin/snippy $rootdir/bin
  echo "------------------------------------------------------------------------------
                            snippy installed
  ------------------------------------------------------------------------------
  "
}

install_kma() {
  echo "------------------------------------------------------------------------------
                            Installing kma
  ------------------------------------------------------------------------------
  "
  wget -c https://bitbucket.org/genomicepidemiology/kma/get/1.2.19.tar.gz -O kma-1.2.19.tar.gz
  tar -xzf kma-1.2.19.tar.gz
  cd genomicepidemiology-kma-*
  make
  cp kma $rootdir/bin/
  cp kma_index $rootdir/bin/
  cp kma_shm $rootdir/bin/
  cp kma_update $rootdir/bin/
  cd $rootdir/thirdParty
  echo "------------------------------------------------------------------------------
                            kma installed
  ------------------------------------------------------------------------------
  "
}

install_muscle() {
  echo "------------------------------------------------------------------------------
                            Installing muscle
  ------------------------------------------------------------------------------
  "
  wget -c https://www.drive5.com/muscle/downloads3.8.31/muscle3.8.31_i86linux64.tar.gz
  tar -xzf muscle3.8.31_i86linux64.tar.gz
  mv muscle3.8.31_i86linux64 muscle
  chmod +x muscle
  cp muscle $rootdir/bin/
  cd $rootdir/thirdParty
  echo "
  ------------------------------------------------------------------------------
                            muscle installed
  ------------------------------------------------------------------------------
  "
}

install_mummer() {
  echo "------------------------------------------------------------------------------
                            Compiling MUMmer3.23 64bit
  ------------------------------------------------------------------------------
  "
  wget -c https://nchc.dl.sourceforge.net/project/mummer/mummer/3.23/MUMmer3.23.tar.gz
  tar -xzf MUMmer3.23.tar.gz
  cd MUMmer3.23
  #for 64bit MUMmer complie
  make CPPFLAGS="-O3 -DSIXTYFOURBITS"
  find . -type f -perm /a+x -exec cp {} $rootdir/bin/ \;
  cd $rootdir/thirdParty
  echo "
  ------------------------------------------------------------------------------
                            MUMmer3.23 compiled
  ------------------------------------------------------------------------------
  "
}

install_bedtools() {
  echo "------------------------------------------------------------------------------
                            Installing bedtools
  ------------------------------------------------------------------------------
  "
  wget -c https://github.com/arq5x/bedtools2/releases/download/v2.29.2/bedtools.static.binary -O bedtools
  cp bedtools $rootdir/bin
  chmod +x $rootdir/bin/bedtools
  echo "------------------------------------------------------------------------------
                            bedtools installed
  ------------------------------------------------------------------------------
  "
}

install_cdhit() {
  echo "------------------------------------------------------------------------------
                            Installing cdhit
  ------------------------------------------------------------------------------
  "
  wget -c https://github.com/weizhongli/cdhit/releases/download/V4.8.1/cd-hit-v4.8.1-2019-0228.tar.gz
  tar -xzf cd-hit-v4.8.1-2019-0228.tar.gz
  cd cd-hit-v4.8.1-2019-0228
  sed -i.bak 's,PREFIX ?= /usr/local,PREFIX ?= '"$rootdir"',' Makefile
  make && make install
  cd $rootdir/thirdParty
  echo "------------------------------------------------------------------------------
                            cdhit installed
  ------------------------------------------------------------------------------
  "
}

install_mcl() {
  echo "------------------------------------------------------------------------------
                            Installing mcl
  ------------------------------------------------------------------------------
  "
  wget -c https://micans.org/mcl/src/mcl-14-137.tar.gz
  tar -xzf mcl-14-137.tar.gz
  cd mcl-14-137
  ./configure --prefix=$rootdir && make && make install
  cd $rootdir/thirdParty
  echo "------------------------------------------------------------------------------
                            mcl installed
  ------------------------------------------------------------------------------
  "
}

install_prank() {
  echo "------------------------------------------------------------------------------
                            Installing prank
  ------------------------------------------------------------------------------
  "
  wget -c http://wasabiapp.org/download/prank/prank.source.170427.tgz
  tar -xzf prank.source.170427.tgz
  cd prank-msa/src && make
  cp prank $rootdir/bin/
  cd $rootdir/thirdParty
  echo "------------------------------------------------------------------------------
                            prank installed
  ------------------------------------------------------------------------------
  "
}

install_mafft() {
  echo "------------------------------------------------------------------------------
                            Installing mafft
  ------------------------------------------------------------------------------
  "
  wget -c https://mafft.cbrc.jp/alignment/software/mafft-7.453-with-extensions-src.tgz
  tar -xzf mafft-7.453-with-extensions-src.tgz
  cd mafft-7.453-with-extensions/core
  sed -i.bak 's,PREFIX = /usr/local,PREFIX = '"$rootdir"',' Makefile
  make && make install
  cd $rootdir/thirdParty
  echo "------------------------------------------------------------------------------
                            mafft installed
  ------------------------------------------------------------------------------
  "
}

install_fasttree() {
  echo "------------------------------------------------------------------------------
                            Installing fasttree
  ------------------------------------------------------------------------------
  "
  wget -c http://www.microbesonline.org/fasttree/FastTree.c
  gcc -DUSE_DOUBLE -O3 -finline-functions -funroll-loops -Wall -o FastTree FastTree.c -lm
  gcc -DOPENMP -DUSE_DOUBLE -fopenmp -O3 -finline-functions -funroll-loops -Wall -o FastTreeMP FastTree.c -lm
  cp FastTree $rootdir/bin/
  cp FastTreeMP $rootdir/bin/
  echo "------------------------------------------------------------------------------
                            fasttree installed
  ------------------------------------------------------------------------------
  "
}

install_roary() {
  echo "------------------------------------------------------------------------------
                            Installing roary
  ------------------------------------------------------------------------------
  "
  install_bedtools
  install_cdhit
  install_mcl
  install_prank
  install_mafft
  install_fasttree
  if ( ! checkSystemInstallation blastn )
  then
    install_BLAST+
  fi
  echo "------------------------------------------------------------------------------
                            roary installed
  ------------------------------------------------------------------------------
  "
}

install_centrifuge() {
  echo "------------------------------------------------------------------------------
                            Installing centrifuge
  ------------------------------------------------------------------------------
  "
  wget -c https://github.com/DaehwanKimLab/centrifuge/archive/v1.0.4-beta.tar.gz -O centrifuge-v1.0.4-beta.tar.gz
  tar -xzf centrifuge-v1.0.4-beta.tar.gz
  cd centrifuge-1.0.4-beta
  sed -i.bak 's,prefix=/usr/local,prefix='"$rootdir"',' Makefile
  make && make install
  cd $rootdir/thirdParty
  echo "------------------------------------------------------------------------------
                            centrifuge installed
  ------------------------------------------------------------------------------
  "
}

install_phage_finder() {
  echo "------------------------------------------------------------------------------
                            Installing phage_finder
  ------------------------------------------------------------------------------
  "
  wget -c https://liquidtelecom.dl.sourceforge.net/project/phage-finder/phage_finder_v2.1/phage_finder_v2.1.tar.gz
  tar -xzf phage_finder_v2.1.tar.gz
  cd $rootdir/thirdParty
  chmod -R +x phage_finder_v2.1
  chmod -R +r phage_finder_v2.1
  echo "------------------------------------------------------------------------------
                            phage_finder installed
  ------------------------------------------------------------------------------
  "
}

install_phylip() {
  echo "------------------------------------------------------------------------------
                            Installing phylip
  ------------------------------------------------------------------------------
  "
  wget -c http://evolution.gs.washington.edu/phylip/download/phylip-3.697.tar.gz
  tar -xzf phylip-3.697.tar.gz
  cd phylip-3.697/src
  make -f Makefile.unx install
  cp ../exe/* $rootdir/bin
  cd $rootdir/thirdParty
  echo "------------------------------------------------------------------------------
                            phylip installed
  ------------------------------------------------------------------------------
  "
}

install_JBrowse() {
  echo "------------------------------------------------------------------------------
                            Installing JBrowse-1.16.6
  ------------------------------------------------------------------------------
  "
  wget -c https://github.com/GMOD/jbrowse/releases/download/1.16.6-release/JBrowse-1.16.6.zip
  unzip -q JBrowse-1.16.6.zip
  if [ -e $rootdir/www/JBrowse/data ]
  then
    mv $rootdir/www/JBrowse/data $rootdir/www/JBrowse_olddata
  fi
  if [ -e $rootdir/www/JBrowse ]
  then
    rm -rf $rootdir/www/JBrowse
  fi
  
  mv JBrowse-1.16.6 $rootdir/www/JBrowse
  cd $rootdir/www/JBrowse
  ./setup.sh
  if [ -e $rootdir/www/JBrowse_olddata ]
  then
    mv $rootdir/www/JBrowse_olddata $rootdir/www/JBrowse/data
  else
    mkdir -p -m 775 data
  fi
  
  ln -s $rootdir/data userdata
  
  cd $rootdir/thirdParty
  #ln -sf $rootdir/thirdParty/JBrowse-1.16.6 $rootdir/www/JBrowse
  echo "
  ------------------------------------------------------------------------------
                            JBrowse-1.16.6 installed
  ------------------------------------------------------------------------------
  "
}

install_circos() {
  echo "------------------------------------------------------------------------------
                            Installing circos-0.69-9
  ------------------------------------------------------------------------------
  "
  wget -c http://circos.ca/distribution/circos-0.69-9.tgz
  tar -xzf circos-0.69-9.tgz
  circosbin=$rootdir/thirdParty/circos-0.69-9/bin/
  ln -fs $circosbin/circos $rootdir/bin
  cd $rootdir/thirdParty
  echo "
  ------------------------------------------------------------------------------
                            circos-0.69-9 installed
  ------------------------------------------------------------------------------
  "
}

checkSystemInstallation() {
  IFS=:
  for d in $PATH; do
    if test -x "$d/$1"; then return 0; fi
  done
  return 1
}

checkLocalInstallation() {
  IFS=:
  for d in $rootdir/bin; do
    if test -x "$d/$1"; then return 0; fi
  done
  return 1
}

containsElement () {
  local e
  for e in "${@:2}"; do [[ "$e" == "$1" ]] && return 0; done
  return 1
}

print_usage() {
cat << EOF
  usage: $0 options
    If no options, it will check existing installation and run tools installation for those uninstalled.
    options:
    help            show this help
    list            show available tools for updates
    tools_name      install/update individual tool
    force           force to install all list tools locally
    
    ex: To update clustalo only
        $0 clustalo
    ex: To update clustalo and prodigal
        $0 clustalo prodigal
    ex: RE-install Alignment tools
        $0 Alignment
        
EOF
}

print_tools_list() {
  echo "Available tools for updates/re-install"
  echo -e "\nAlignment"
  for i in "${alignments_tools[@]}"
  do
    echo "* $i"
  done
  echo -e "\nAnalysis"
  for i in "${analysis_tools[@]}"
  do
    echo "* $i"
  done
  echo -e "\nAnnotation"
  for i in "${annotation_tools[@]}"
  do
    echo "* $i"
  done
  echo -e "\nClassification"
  for i in "${classification_tools[@]}"
  do
    echo "* $i"
  done
  echo -e "\nPhylogeny"
  for i in "${phylogeny_tools[@]}"
  do
    echo "* $i"
  done
  echo -e "\nUtility"
  for i in "${utility_tools[@]}"
  do
    echo "* $i"
  done
}

### Main ####
if [ "$#" -ge 1 ]
then
  for f in $@
  do
    case $f in
      help)
        print_usage
        exit 0;;
      list)
        print_tools_list
        exit 0;;
      Alignment)
        for tool in "${alignments_tools[@]}"
        do
          install_$tool
        done
        echo -e "Alignment tools installed.\n"
        exit 0;; 
      Analysis)
        for tool in "${analysis_tools[@]}"
        do
          install_$tool
        done
        echo -e "Analysis tools installed.\n"
        exit 0;; 
      Annotation)
        for tool in "${annotation_tools[@]}"
        do
          install_$tool
        done
        echo -e "Annotation tools installed.\n"
        exit 0;; 
      Classification)
        for tool in "${classification_tools[@]}"
        do
          install_$tool
        done
        echo -e "Classification tools installed.\n"
        exit 0;; 
      Phylogeny)
        for tool in "${phylogeny_tools[@]}"
        do
          install_$tool
        done
        echo -e "Phylogeny tools installed.\n"
        exit 0;; 
      Utility)
        for tool in "${utility_tools[@]}"
        do
          install_$tool
        done
        echo -e "Utility tools installed.\n"
        exit 0;; 
      force)
        for tool in "${all_tools[@]}"
        do
          install_$tool
        done
        ;;
      *)
        if ( containsElement "$f" "${annotation_tools[@]}" || containsElement "$f" "${analysis_tools[@]}" || containsElement "$f" "${alignments_tools[@]}" || containsElement "$f" "${classification_tools[@]}" || containsElement "$f" "${phylogeny_tools[@]}" || containsElement "$f" "${utility_tools[@]}" )
        then
          install_$f
        else
          echo "$f: invalid tool"
          print_tools_list
        fi
        exit;;
    esac
  done
fi

if $rootdir/bin/python -c 'import Bio; print Bio.__version__' >/dev/null 2>&1
then
  $rootdir/bin/python -c 'import Bio; print "BioPython Version", Bio.__version__, "is found"'
else
  echo "Anaconda2 is not found"
  install_Anaconda2
fi

if ( checkSystemInstallation snippy )
then
  echo "snippy is found"
else
  echo "snippy is not found"
  install_snippy
fi

if ( checkSystemInstallation clustalo )
then
  echo "clustalo is found"
else
  echo "clustalo is not found"
  install_clustalo
fi

if ( checkSystemInstallation roary )
then
  echo "roary is found"
else
  echo "roary is not found"
  install_roary
fi

if ( checkSystemInstallation blastn )
then
  echo "BLAST+ is found"
else
  echo "BLAST+ is not found"
  install_BLAST+
fi

if ( checkSystemInstallation blastall )
then
  echo "blastall is found"
else
  echo "blastall is not found"
  install_blastall
fi

if ( checkSystemInstallation prodigal )
then
  echo "prodigal is found"
else
  echo "prodigal is not found"
  install_prodigal
fi

if [ -x $rootdir/www/JBrowse/bin/prepare-refseqs.pl ]
then
  echo "JBrowse is found"
else
  echo "JBrowse is not found"
  install_JBrowse
fi

cd $rootdir

if [ -f $HOME/.bashrc ]; then {
  echo "# Added by HPDB pipeline installation" >> $HOME/.bashrc
  echo "export HPDB_BASE=$rootdir" >> $HOME/.bashrc
  echo "export PATH=$rootdir/bin:$rootdir/thirdParty/Anaconda2/bin:\$PATH:" >> $HOME/.bashrc
  echo "export PYTHONPATH=$rootdir/scripts:\$PYTHONPATH:" >> $HOME/.bashrc
  echo "alias httperr='sudo cat /var/log/apache2/error.log'" >> $HOME/.bashrc
  echo "alias httperrclear='sudo sh -c "'"'"echo '' > /var/log/apache2/error.log"'"'"'" >> $HOME/.bashrc
  #echo "alias httperr='sudo cat /etc/httpd/logs/error_log'" >> $HOME/.bashrc
  #echo "alias httperrclear='sudo sh -c "'"'"echo '' > /etc/httpd/logs/error_log"'"'"'" >> $HOME/.bashrc
} else {
  echo "# Added by HPDB pipeline installation" >> $HOME/.bash_profile
  echo "export HPDB_BASE=$rootdir" >> $HOME/.bash_profile
  echo "export PATH=$rootdir/bin:$rootdir/thirdParty/Anaconda2/bin:\$PATH:" >> $HOME/.bash_profile
  echo "export PYTHONPATH=$rootdir/scripts:\$PYTHONPATH:" >> $HOME/.bash_profile
  echo "alias httperr='sudo cat /var/log/apache2/error.log'" >> $HOME/.bash_profile
  echo "alias httperrclear='sudo sh -c "'"'"echo '' > /var/log/apache2/error.log"'"'"'" >> $HOME/.bash_profile
  #echo "alias httperr='sudo cat /etc/httpd/logs/error_log'" >> $HOME/.bash_profile
  #echo "alias httperrclear='sudo sh -c "'"'"echo '' > /etc/httpd/logs/error_log"'"'"'" >> $HOME/.bash_profile
}
fi

echo "* * * * * ( $rootdir/make-run.sh &>/dev/null & )" | crontab -

echo "All done! Run 'exec bash' to restart your terminal session."
