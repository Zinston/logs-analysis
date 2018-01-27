
# Logs Analysis

Prints out reports based on the analysis of a newspaper's database.

## Usage

The reports answer the following questions:

* What are the most popular three articles of all time?
* Who are the most popular article authors of all time?
* On which days did more than 1% of requests lead to errors?

## Installation

### Virtual machine

_Logs Analysis_ makes use of a Virtual machine that can be installed as follows:

* Install [VirtualBox 5.1](https://www.virtualbox.org/wiki/Download_Old_Builds_5_1)
* Install [Vagrant](https://www.vagrantup.com/downloads.html)
* Download the [VM configuration](https://d17h27t6h515a5.cloudfront.net/topher/2017/August/59822701_fsnd-virtual-machine/fsnd-virtual-machine.zip)
* Start the virtual machine: 
	* `cd vagrant ` to open the vagrant subdirectory
	* `vagrant up` to download and install the Linux operating system
	* `vagrant ssh` to log in to the virtual machine

### Database

_Logs Analysis_ analyses the data from a database that can be downloaded and initialized as follows:

* [Download the data](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip)
* Unzip the archive and move `newsdata.sql` to the vagrant subdirectory
* Within the vagrant subdirectory: `psql -d news -f newsdata.sql` to initalize the database
* Move `views.sql` to the vagrant subdirectory
* Create views in the database: `psql -d news -f views.sql`

## Running the reports

Once everything is installed: `python analysis.py`