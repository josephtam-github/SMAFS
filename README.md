<!-- Back to Top Navigation Anchor -->
<a name="readme-top"></a>

<!-- Project Shields -->
<div align="center">

  [![Contributors][contributors-shield]][contributors-url]
  [![Forks][forks-shield]][forks-url]
  [![Stargazers][stars-shield]][stars-url]
  [![Issues][issues-shield]][issues-url]
  [![MIT License][license-shield]][license-url]
  [![Twitter][twitter-shield]][twitter-url]
</div>

<!-- Project Name -->
<div align="center">
  <h1>SMAFS</h1>
</div>

<div>
  <p align="center">
    <a href="https://github.com/josephtam-github/SMAFS#readme"><strong>Explore the Docs »</strong></a>
    <br />
    <a href="/images/SMAFS_Full_Page.png">View Demo</a>
    ·
    <a href="https://github.com/josephtam-github/SMAFS/issues">Report Bug</a>
    ·
    <a href="https://github.com/josephtam-github/SMAFS/issues">Request Feature</a>
  </p>
</div>

---

<!-- Table of Contents -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-SMAFS">About SMAFS</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li><a href="#lessons-learned">Lessons Learned</a></li>
    <li><a href="#usage">Usage</a></li>    
    <li><a href="#sample">Sample</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgements">Acknowledgements</a></li>
  </ol>
  <p align="right"><a href="#readme-top">back to top</a></p>
</details>

---

<!-- About the Project -->
## About Ze School

SMAFS is an API built with Flask-Smorest, designed to facilitate account registration and student data management for school admin on a web application powered by PythonAnywhere. The API provides capabilities to Create, Read, Update, and Delete student data, and features a user-friendly Swagger UI that makes testing and front-end integration easy.

Access to the web application is limited for students, who can only view and modify their own profile details, as well as view information about their courses, grades, and CGPA.

This student management API was built with Python's Flask-Smorest by <a href="https://www.github.com/josephtam-github">Joseph Tam</a> during Backend Engineering third semester exam at <a href="https://altschoolafrica.com/schools/engineering">AltSchool Africa</a>.

<p align="right"><a href="#readme-top">back to top</a></p>

### Built With:
* [Python 3](https://www.python.org/download/releases/3.0/) - The language programming used
* [Flask](http://flask.pocoo.org/) - The web framework used
* [Flask Migrate](https://pypi.org/project/Flask-Migrate/) - The database migration
* [Virtualenv](https://virtualenv.pypa.io/en/latest/) - The virtual environment used
* [Flask-smorest](https://flask-smorest.readthedocs.io/en/latest/) - A database-agnostic framework library for creating REST APIs.
* [SQL Alchemy](https://www.sqlalchemy.org/) - The database library
* [Flask-SQLAlchemy](http://flask-sqlalchemy.pocoo.org/2.3/) - Flask and SQL Alchemy connector
* [flask-marshmallow](https://flask-marshmallow.readthedocs.io/) - Integration layer for Flask and marshmallow (an object serialization/deserialization library)
* [PyJWT](https://pyjwt.readthedocs.io/) - Python library which allows you to encode and decode JSON Web Tokens

<p align="right"><a href="#readme-top">back to top</a></p>

---
<!-- Lessons from the Project -->
## Lessons Learned

* Creating this API helped me learn and practice:
* Developing APIs using Python programming language
* Deploying applications with PythonAnywhere
* Testing the application using Insomnia and pytest
* Creating documentation for the application
* Debugging the application to fix errors
* Establishing routes for user requests
* Managing databases for the application
* Ensuring internet security for the application
* Implementing user authentication features
* Granting user authorization for accessing different features of the application.

<p align="right"><a href="#readme-top">back to top</a></p>

---

<!-- GETTING STARTED -->
## Usage

To use this API, follow these steps:

1. Open the PythonAnywhere web app on your browser: https://josephtam.pythonanywhere.com

------------------------------------------------------------------------------------------

2. Create an admin or student account:
    - Click 'auth' to reveal a dropdown menu of authentication routes, then register an admin account via the <code>/auth/register</code> route <br> <b> Note: The first account you register will be the only admin account </b>
    - Click 'auth' once again then register a student account via the <code>/students/register</code> route

------------------------------------------------------------------------------------------

3. Sign in via the '/auth/login' route to generate a JWT token. Copy this access token without the quotation marks

------------------------------------------------------------------------------------------

4. Scroll up to click 'Authorize' at top right. Enter the JWT token in the given format, for example:
   ```
   Bearer this1is2a3rather4long5hex6string
   ```

5. Click 'Authorize' and then 'Close'

------------------------------------------------------------------------------------------

6. Now authorized, you can create, view, update and delete students, courses, and grades via the many routes in 'students', 'courses' and 'record'. You can also get:
    - List of students enrolled in a specific course.
    - List of courses taken by a particular student.
    - A student's grade, presented as a percentage (e.g. 92.3%) or as a letter grade (e.g. B).
    - A student's CGPA, which is determined by calculating the average grade from all the courses they have taken.

------------------------------------------------------------------------------------------

7. When you're done, click 'Authorize' at top right again to then 'Logout'
 
**Note:**
   - When using this API in production live, there is only one admin with details: 
        <br> <code> name: admin@altcshool.com</code> 
        <br> <code>password: password</code> 
        <br> To login as an admin you need to supply the following JSON to <code>auth/login</code>: <br>
        <code>{"email":"admin@altschool.com", "password":"password"}</code>
        <br>
   - The password for all students generated is: <code>password</code>
    

<p align="right"><a href="#readme-top">back to top</a></p>

---

<!-- Sample Screenshot -->
## Sample

<br>

[![SMAFS Screenshot][SMAFS-screenshot]](https://github.com/josephtam-github/SMAFS/blob/main/images/SMAFS_Full_Page.png)

<br>

[![SMAFS Posterman][SMAFS-screenshot]](https://github.com/josephtam-github/SMAFS/blob/main/images/Posterman.png)

<br>

<p align="right"><a href="#readme-top">back to top</a></p>

---

<!-- License -->
## License

Distributed under the MIT License. See <a href="https://github.com/josephtam-github/SMAFS/blob/main/LICENSE">LICENSE</a> for more information.

<p align="right"><a href="#readme-top">back to top</a></p>

---

<!-- Contact -->
## Contact

Joseph Tam Ogbo - [@Joseph_tam](https://twitter.com/Joseph_tam_) - josephtam247@gmail.com

Project Link: [SMAFS](https://github.com/josephtam-github/SMAFS)

<p align="right"><a href="#readme-top">back to top</a></p>

---

<!-- Acknowledgements -->
## Acknowledgements

This project was made possible by:

* [AltSchool Africa School of Engineering](https://altschoolafrica.com/schools/engineering)
* [Caleb Emelike's Flask Lessons](https://github.com/CalebEmelike)

<p align="right"><a href="#readme-top">back to top</a></p>

---

<!-- Markdown Links & Images -->
[contributors-shield]: https://img.shields.io/github/contributors/josephtam-github/SMAFS.svg?style=for-the-badge
[contributors-url]: https://github.com/josephtam-github/SMAFS/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/josephtam-github/SMAFS.svg?style=for-the-badge
[forks-url]: https://github.com/josephtam-github/SMAFS/network/members
[stars-shield]: https://img.shields.io/github/stars/josephtam-github/SMAFS.svg?style=for-the-badge
[stars-url]: https://github.com/josephtam-github/SMAFS/stargazers
[issues-shield]: https://img.shields.io/github/issues/josephtam-github/SMAFS.svg?style=for-the-badge
[issues-url]: https://github.com/josephtam-github/SMAFS/issues
[license-shield]: https://img.shields.io/github/license/josephtam-github/SMAFS.svg?style=for-the-badge
[license-url]: https://github.com/josephtam-github/SMAFS/blob/main/LICENSE.txt
[twitter-shield]: https://img.shields.io/badge/-@josephtam-github-1ca0f1?style=for-the-badge&logo=twitter&logoColor=white&link=https://twitter.com/Joseph_tam_
[twitter-url]: https://twitter.com/josephtam-github
[SMAFS-screenshot]: https://github.com/josephtam-github/SMAFS/blob/main/images/SMAFS_Full_Page.png
[python]: https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54
[flask]: https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white
[sqlite]: https://img.shields.io/badge/sqlite-%2307405e.svg?style=for-the-badge&logo=sqlite&logoColor=white