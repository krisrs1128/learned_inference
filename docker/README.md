
These are docker images that are used in the condor jobs in the `run_scripts`
directory. `docker_base` contains basic R and python libraries.
`docker_project_deps` includes some libraries that are more specialized to this
project, but which we wouldn't want to rebuild every time we make a small change
to our package. Our package itself is installed in `docker_project`.

To build any one of these docker images, you can use

```
docker build . --file docker_***
```

For the `docker_project` install, it can be good to include the `--no-cache`
flag as well. This will redownload the updated package from github (otherwise it
will use an old version in the cache).
