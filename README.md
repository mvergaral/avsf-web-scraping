# Python Web Scraping

## [Guía comandos terminal](./BASH_GUIDE.md)
## Setup (Mac)

Ejecutar los siguientes comandos desde la terminal (la terminal integrada de OSX sirve, pero se recomienda el uso de [Hyper](https://hyper.is/).

### 1.- Instalar Xcode

```console
xcode-select —-install
```

 Si aparece un error ejecutar

```console
xcode-select -r
```

 intentar nuevamente

### 2.- Instalar Homebrew

 Hombrew es basicamente un gestor de paquete para OSX muy util

```console
/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
```

### 3.- Instalar ZSH

 Lenguaje de scripting, básicamente bash con esteroides

```console
brew install zsh
```

### 4.- Instalar Oh-my-zsh

 Es un framework de gestión de configuración para zsh

```console
sh -c "$(curl -fsSL https://raw.githubusercontent.com/robbyrussell/oh-my-zsh/master/tools/install.sh)"
```

### 5.- Instalar Python

 Para instalar python ocuparemos brew, ejecutar

```console
brew install python
```

### 6.- Instalar Miniconda (o Anaconda si se desea)

 Para poder instalar paquetes de python y crear entornos de trabajo

```console
brew install --cask miniconda
```

### 7.- Instalar geckodriver y chromedriver

 Es necesario para utilizar webdrivers con Selenium

```console
brew install geckodriver && brew install chromedriver --cask
```

### 8.- Crear el entorno de web scraping

 Contiene los paquetes mínimos necesarios como [BeatifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/#making-the-soup) y [Selenium](https://selenium-python.readthedocs.io/). Para crear el entorno ejecutar el siguiente comando desde dentro de la carpeta del repositorio

```console
conda env create -f environment.yml
```
