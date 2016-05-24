### File Structure

* src/
    * templates/
    * pages/
    * posts/
* output/
    * pages/
        * about.html
        * resume.html
        * etc
    * posts/
        * $(uuid-gen)
        * etc
    * index.html
* siteconfig.(yml|json)

## Generate the Site

* Create a directory called `.out.staging`
* Write all content inside `.out.staging`
* Move to `out`
