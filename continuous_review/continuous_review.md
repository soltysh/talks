## Continuous Review Jenkins & Sonar ##

### Maciej Szulik ###

### soltysh @ <i class="fa-twitter"></i><i class="fa-github"></i><i class="fa-bitbucket"></i> ###

Katowice, 2013

## TOC ##

* Continuous Integration
* Code review
* Demo

## Continuous Integration ##

* XP
* Merging working copies several times a day
* Prevent integration problems - "integration hell"
* TDD
* Build server, which automatically run the unit tests periodically or after 
  every commit and report the results

&nbsp;

[http://en.wikipedia.org/wiki/Continuous_integration](http://en.wikipedia.org/wiki/Continuous_integration)

## CI Advantages ##

* Immediate unit testing
* Detect and fix integration problems continuously
* Early warning of broken/incompatible code
* Early warning of conflicting changes
* Constant availability of a "current" build
* Immediate feedback to developers on the quality
* Less complex code
* Metrics

## CI Disadvantages ##

* Initial setup time required
* Well-developed test-suite

## Meet Jenkins ##

* Hudson in Feb. 2005
* Jenkins in Jan 2011
* Java
* Open source (MIT License)

## Tasks ##

* Building/testing software projects continuously
* Monitoring executions of externally-run jobs

&nbsp;

[https://wiki.jenkins-ci.org/display/JENKINS/Meet+Jenkins](https://wiki.jenkins-ci.org/display/JENKINS/Meet+Jenkin)

## Features ##

* Easy installation & configuration
* Changelog
* Permanent links
* RSS/E-mail/IM integration
* After-the-fact tagging
* Distributed builds
* File fingerprinting
* Plugin support

&nbsp;

[https://wiki.jenkins-ci.org/display/JENKINS/Meet+Jenkins](https://wiki.jenkins-ci.org/display/JENKINS/Meet+Jenkin)

## Workflow ##

* Checkout from SCM
* Pre-build steps
* Build
* Post-build steps
* Post-build actions

## Jenkins Demo ##

![Jenkins](img/jenkins.png)\ 

## Code review ##

* Systematic examination of source code
* Remove common vulnerabilities
* Improve quiality of software and the developers' skills

&nbsp;

[http://en.wikipedia.org/wiki/Code_review](http://en.wikipedia.org/wiki/Code_review)

## CR Types ##

* Over-the-shoulder
* Email pass-around
* Pair programming
* Tool-assisted code review

&nbsp;

[http://en.wikipedia.org/wiki/Code_review](http://en.wikipedia.org/wiki/Code_review)

## CR python Tools ##

* pep8
* pylint
* pyflakes
* pychecker
* coverage

## Sonarqube ##

* At a glance
* For all stakeholder
* Seven Deadly Sins
* Language support
* Time machine
* Stop the leak
* Pre-commit check
* Zoom to the source
* Automate
* Security
* Extend
* Integrate

&nbsp;

[http://www.sonarqube.org/](http://www.sonarqube.org/)

## Sonar demo ##

![Sonarqube](img/sonarqube.png)\ 

## Integrate, integrate, integrate... ##

![Jenkins](img/jenkins.png)
![Sonarqube](img/sonarqube.png)

## Questions? ##

### Maciej Szulik ###

### soltysh @ <i class="fa-twitter"></i><i class="fa-github"></i><i class="fa-bitbucket"></i> ###

