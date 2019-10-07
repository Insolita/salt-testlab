# Local salt state testing environment
Inspired by https://github.com/amolenaar/salt-formula-testing but use more fresh environment
- debian9, debian10, ubuntu18.04
- salt 2019.2
- python3

### Directory structure:

/

  _docker/   - docker images

  _vagrant/  - vagrant server with salt

      salt/      - salt config provision

  suites/    - base dir for suites (sets of states or formulas)

     demo/   - simple demo suite

  tests/     - base dir for tests
  



### Usage

- Clone project on your local machine (next i assume that your repo clonned into salt-testlab)


  **Run on local machine without Vagrant**
   - Ensure that you have installed 
      - docker
      - salt 
      - python3
      - pip3
      - testinfra
      - pytest

  
   **Run with Vagrant**
   (vagrant provide preconfigured env with masterless salt and testinfra)

   - run `cd salt-testlab/_vagrant && vagrant up`
   - enter in vagrant machine: `vagrant ssh`

- `cd salt-testlab`

- Run existed tests 
   - `py.test -v -s tests/test_self`
   - `py.test -v -s tests/test_demo`

- Put own formulas in suites folder 
  
  each suite structure should be as
     sutenameX/
           pillar
           states
           ...
           modules
           ...
           top.sls

    

  
### Useful Docs 

- http://doc.pytest.org/en/latest/usage.html

- https://testinfra.readthedocs.io/en/latest/index.html