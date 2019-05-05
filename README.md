# SwiftVuln
<h1 align="center">
  <br />
  <img src="./assets/buttons/logo_blue.png" alt="icon" width="450px" />
  <br/>
  <br/>
  SwiftVuln
  <br/>
  <img src="https://img.shields.io/badge/python-2.7.16-green.svg" />
  <br/>
</h1>
<h4 align="center">A Network Security Quantifier</h4>

**It is highly recommended for the application to be run on Kali Linux.**
# Application Dependencies

1. Check if you already have OpenVAS 9 on your desktop.

  ```
  openvas-check-setup
  ```
2. If not, install OpenVAS 9 on your desktop. For linux users here's how:
  ```
  sudo apt-get install openvas
  ```
3. Now install all the dependencies from requirements.txt
  ```
  sudo pip install -r requirements.txt
  ```
### Running the application
  ```
  python app.py
  ```