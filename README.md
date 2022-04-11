# VSCO Gallery Parser

## Overview
This program is intended to gather VSCO images from my personal VSCO account, but it can be used with any public account. 
Due to VSCO not having an open API I needed to do a bit of reverse engineering to figure out the endpoints I needed to access
in order to be able to do this.

### Routes on the VSCO Website:
| Request                                                                      | Description                                           |
|------------------------------------------------------------------------------|-------------------------------------------------------|
| GET https://vsco.co/content/Static/userinfo?callback=60                      | VSCO Session Cookie called `vs`                       |
| GET https://vsco.co/ajxp/{$vs_goes_here}/2.0/sites?subdomain={$account_name} | The `id` field is needed from `sites`                 |
 | GET https://vsco.co/ajxp/{$vs_goes_here}/2.0/medias?site_id={$site_id}       | This endpoint returns your all your photos and videos |

Using these routes allow me to download all my images from my VSCO account and tag them with the tags I have posted the
photo with.This then allows me to set up a route on my own server to return photos to my portfolio website.

## Requirements
Python 3.8+

## Usage


## References
* https://vsco.co/