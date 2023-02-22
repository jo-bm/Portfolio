
# Electify app

## the app
Electify is a web application built using the Flask web framework in Python. The app is designed to allow users to view information about political parties and vote for their preferred party.

The app includes several pages, such as a home page that displays a list of political parties, a party page that provides detailed information about a selected party, and a login page that allows an administrator to access an admin page.
(The parties data automaticlly collected from a CSV file that i found online)

The home page displays a list of political parties that are stored in a MySQL database, and users can click on a party to view more detailed information on the party page. The party page displays the name and platform of the selected party,
Users can also vote for their preferred party on the party page, but only if they are eligible to vote and have not already voted.
The app checkes the database for the user's id, eligiblity to vote, and voted / not-voted status

The app also includes an admin page that is accessible through the login page. The admin page allows an administrator to add or delete political parties, as well as download a CSV file containing information about the users.

My Flask App is designed to be user-friendly, secure, scalable, and includes several custom design elements and animations to enhance the user experience. It is built using HTML, CSS, and JavaScript for the front-end, and Python and MySQL for the back-end.

![screenshot](https://i.imgur.com/IjFQtf9.jpg)

## CI/CD Architecture


![screenshot](https://i.imgur.com/BeWDEYb.jpg)

When a developer pushes changes to the GitHub repository, a CI pipeline is triggered automatically.
If the changes are made to the master branch, the CI pipeline sets up the three-tier application environment,
including Flask, MySQL, and Nginx, in a containerized environment with network isolation.
Then, it runs full end-to-end tests on the application to ensure that it is working as expected.

If the changes are made to a feature branch, the CI pipeline skips the folowing steps and goes directly to the report step.
If the end-to-end tests are successful, the CI pipeline automatically calculates a semantic versioning tag and pushes it to GitHub.
As well publish the images to dockerhub

In the CD phase, the CI pipeline edits the tag in the YAML files of a private other GitLab repository.
These YAML files contain the deployment configurations for the Kubernetes architecture, such as deployment, stateful set, services, volumes, and other components.

Meanwhile, in the GKE cluster, an instance of ArgoCD is listening to the GitLab repository, waiting patiently for changes. 
When a change is made to the YAML files, Argo deploys the updated configurations to the Kubernetes cluster automatically, ensuring that the application is always up to date and running.

The last step in the CI/CD pipeline is the reporting phase,
which is designed to provide developers with real-time feedback on the status of the pipeline. 
The pipeline sends a Telegram push that includes detailed information on the completion status of the pipeline, 
such as whether the tests have passed or failed, whether a new version has been deployed, link to the fully ci/cd reports,
and any other relevant information that might be useful to the developers. 
This ensures that developers are always up to date with the latest changes and can take appropriate action if necessary.



## Tools i used in this project

<table>
  <tr>
    <td align="center"><a href="https://git-scm.com/"><img src="https://cdn3.iconfinder.com/data/icons/social-media-2169/24/social_media_social_media_logo_git-512.png" width="75px;" height="75px;" alt="Git" /><br /><b>Git</b></a></td>
    <td align="center"><a href="https://kubernetes.io/"><img src="https://cdn2.iconfinder.com/data/icons/mixd/512/16_kubernetes-512.png" width="75px;" height="75px;" alt="Kubernetes"/><br /><b>Kubernetes</b></a></td>
    <td align="center"><a href="https://www.python.org/"><img src="https://cdn3.iconfinder.com/data/icons/logos-and-brands-adobe/512/267_Python-512.png" width="75px;" height="75px;" alt="Python"/><br /><b>Python</b></a></td>
    <td align="center"><a href="https://flask.palletsprojects.com/"><img src="https://e7.pngegg.com/pngimages/509/951/png-clipart-flask-by-example-web-framework-python-bottle-bottle-text-logo-thumbnail.png" width="75px;" height="75px;" alt="Flask"/><br /><b>Flask</b></a></td>
    <td align="center"><a href="https://www.gnu.org/software/bash/"><img src="https://cdn3.iconfinder.com/data/icons/logos-brands-3/24/logo_brand_brands_logos_linux-128.png" width="75px;" height="75px;" alt="Bash"/><br /><b>Shell Scripting</b></a></td>
  </tr>
  <tr>
    <td align="center"><a href="https://cloud.google.com/"><img src="https://static-00.iconduck.com/assets.00/google-cloud-platform-icon-512x455-f8ws1zg7.png" width="70px;" height="70px;" alt="Google Cloud Platform"/><br /><b>Google Cloud Platform</b></a></td>
    <td align="center"><a href="https://www.mysql.com/"><img src="https://cdn4.iconfinder.com/data/icons/logos-3/181/MySQL-512.png" width="75px;" height="75px;" alt="MySQL"/><br /><b>MySQL</b></a></td>
    <td align="center"><a href="https://github.com/"><img src="https://cdn4.iconfinder.com/data/icons/ionicons/512/icon-social-github-512.png" width="75px;" height="75px;" alt="GitHub"/><br /><b>GitHub</b></a></td>
    <td align="center"><a href="https://about.gitlab.com/"><img src="https://cdn4.iconfinder.com/data/icons/logos-and-brands/512/144_Gitlab_logo_logos-512.png" width="75px;" height="75px;" alt="GitLab"/><br /><b>GitLab</b></a></td>
    <td align="center"><a href="https://argoproj.github.io/argo-cd/"><img src="https://cncf-branding.netlify.app/img/projects/argo/icon/color/argo-icon-color.png" width="80px;" height="80px;" alt="ArgoCD"/><br /><b>ArgoCD</b></a></td>
  </tr>
  <tr>
    <td align="center"><a href="https://nginx.org/"><img src="https://cdn4.iconfinder.com/data/icons/logos-brands-5/24/nginx-512.png" width="75px;" height="75px;" alt="Nginx"/><br /><b>Nginx</b></a></td>
    <td align="center"><a href="https://helm.sh/"><img src="https://helm.sh/img/helm.svg" width="75px;" height="75px;" alt="Helm"/><br /><b>Helm</b></a></td>
    <td align="center"><a href="https://developer.mozilla.org/en-US/docs/Web/HTML"><img src="https://cdn1.iconfinder.com/data/icons/logotypes/32/badge-html-5-512.png" width="75px;" height="75px;" alt="HTML"/><br /><b>HTML</b></a></td>
    <td align="center"><a href="https://developer.mozilla.org/en-US/docs/Web/JavaScript"><img src="https://cdn1.iconfinder.com/data/icons/ionicons-fill-vol-2/512/logo-javascript-512.png" width="75px;" height="75px;" alt="JavaScript"/><br /><b>JavaScript</b></a></td>
    <td align="center"><a href="https://www.gnu.org/software/bash/"><img src="https://cdn4.iconfinder.com/data/icons/proglyphs-computers-and-development/512/Terminal-512.png" width="75px;" height="75px;" alt="Bash"/><br /><b>Shell Scripting</b></a></td>

  </tr>

</table>