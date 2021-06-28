import click
import sys,os
from datetime import datetime
import subprocess
import errno
from string import punctuation

@click.command()
def cli():
    section = click.prompt("Enter section name (ex: Data_Modeling)")
    section = slug_section(section.title())
    lesson = click.prompt("Enter Lesson,(ex: 01)")
    title = click.prompt("Title name of the Concept Section(ex. What is Data Modeling?")
    title_clean = clean_title(title.title())
    bg_slug = slug_title(title_clean)  # create slug
    dir = make_dirs(section,lesson)
    md_temp = template()  # load empty template function
    fill_md(md_temp,section, lesson,title_clean,dir,bg_slug)  # load empty template with data and save
    click.echo(f'Your title is: {title}')

def template():
    
    post_template ="""
# Section: {section}
# Lesson: {lesson}
# {title}
## {year}-{month}-{day}
---
"""
    return post_template

def clean_title(title):
    '''Clean the title'''
    rem_pun = ''.join(
        c for c in title if c not in punctuation)  # remove punctuations
    clean_title = ' '.join(rem_pun.split())  # remove spaces
    return clean_title

def slug_section(section):
    '''slug section '''
    slug = section.strip().replace(' ', '_')
    return slug

def slug_title(title):
    '''slug the title'''
    slug = title.lower().strip().replace(' ', '-')
    return slug
    
# content/section/lesson_xx/
def make_dirs(section,lesson):
    '''create directories'''
    #content
    notes_dir ='content'
    if not os.path.exists(notes_dir):
        os.makedirs(notes_dir)
       # print("{}/\tCREATED".format(notes_dir))
    
    # section
    section_dir ='{}/{}'.format(notes_dir,section)
    if not os.path.exists(section_dir):
        os.makedirs(section_dir)

    # lesson section
    lession_sec = '{}/Lesson_{}'.format(section_dir,lesson)
    if not os.path.exists(lession_sec):
        os.makedirs(lession_sec)
        #print("{}/{}/{}\tCREATED".format(notes_dir,part,module))
        print('{}'.format(lession_sec))

    return lession_sec

def fill_md(md_temp,section,lesson, title_clean, dir, slug):
    today = datetime.today()
    # content/section/lesson_xx/concepts.md
    md_file = "{}/{}.md".format(dir,slug)
    md_post = md_temp.strip().format(section = section, 
                                    lesson = lesson,
                                    title=title_clean.title(),
                                     year=today.year,
                                     month='{:02d}'.format(today.month),
                                     day='{:02d}'.format(today.day))
    if not os.path.exists(md_file):
        with open(md_file, 'w') as w:
            w.write(md_post)
        print("{}\tCREATED".format(md_file))
    else:
        print('{}\tEXIST'.format(md_file))

if __name__ =='__main__':
    cli()