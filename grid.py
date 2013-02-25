#!/usr/bin/env python
import os
import yaml
import jinja2
import distutils.dir_util

def process_post(blog_config, file):
    template = env.get_template('post.html')
    
    with open("posts/" + file) as fd:
        fname = os.path.splitext(file)[0]
        post = yaml.safe_load_all(fd)
        metadata = post.next()
        post_contents = post.next()
        with open("output/" + fname + ".html", "w+") as out:
            out.write(template.render(blog_config=blog_config, metadata=metadata, post_contents=post_contents))

    return metadata


def create_index(blog_config, metadata_list):
    template = env.get_template('index.html')

    with open("output/index.html", "w+") as out:
        out.write(template.render(blog_config = blog_config, posts_metadata = metadata_list))

env = jinja2.Environment(loader=jinja2.PackageLoader('grid', 'templates'))

if __name__ == "__main__":
    blog_config = None

    try:
        with open("blog.yaml") as fd:
            blog_config = yaml.safe_load_all(fd)
    except IOError:
        print "unable to open blog config file 'blog.yaml'."
        os.exit(-1)


    metadata_list = []

    if not os.path.exists("output") and os.path.isdir("output"):
        print "output/ directory doesn't exists"
        os.exit(-1)
    
    print "Copying static files"
    distutils.dir_util.copy_tree("static", "output/")

    print "Generating post pages"
    for file in os.listdir('posts/'):
        ext = os.path.splitext(file)[1]
        if ext in [".yaml"] and file[0] != ".":
            metadata_list.append(process_post(blog_config, file))

    print "Creating index.html"
    create_index(blog_config, metadata_list)
