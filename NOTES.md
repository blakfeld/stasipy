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

## Post Summary

* Need a Jinja extention to generate post summaries

## Images

* Need a Jinja extention to generate image tags.

## Meta Documents

* Documents that get rendered after everything else, and one I make
    fewer assumptions about.
