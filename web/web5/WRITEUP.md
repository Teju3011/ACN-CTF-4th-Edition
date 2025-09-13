## Writeup

- register a user  in the website
- check the cookie using burpsuite or cookie editor
- decode the base64 encoded auth cookie with name auth
- change the role of current user to admin and base64 encode it
- send the encoded cookie with a request to dashboard.html either by using burpsuite or by changing the auth field from cookie editor
- This should give you the flag 