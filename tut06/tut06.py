"""
@author: mayank64ce
The following program renames tv series name to more human readable names.
"""
import os
import re
import shutil

WRONG_PATH = 'wrong_srt'
CWD = os.path.dirname(os.path.realpath(__file__))
CORRECT_PATH = 'corrected_srt'


def get_padding(name, padding):
    """
    This method prepends name with 0s to a length of padding

    Args:
            name ([string]): [string to be padded]
            padding ([int]): [padding]

    Returns:
            [string]: [the padded string]
    """

    if len(name) > padding:
        return name

    times = padding - len(name)

    return times*'0' + name


def get_episode_name(name, season_number, episode_number, episode_name, season_padding, episode_padding):
    """This method generates the name of the episode file based on the show, season and episode numbers.

    Args:
            name (string): name of the show
            season_number (string): season number in string format without leading zeroes
            episode_number (string): episode number in string format without leading zeroes
            episode_name (string): name of the episode
            season_padding (int): season padding to be used
            episode_padding (int): episode padding to be used

    Returns:
            string: name of the file
    """
    season = get_padding(season_number, season_padding)
    episode = get_padding(episode_number, episode_padding)
    filename = (name + ' - ' + 'Season ' + season +
                ' Episode ' + episode)
    if len(episode_name) > 0:
        filename += ' - ' + episode_name
    return filename


def get_filename(filename, name, show, season_padding, episode_padding):
    """
            This method extracts the season number, episode number
            and episode from the filename and returns the full filename of the
            corrected file.

            Args:
                    filename (string): full filename
                    name (string): name of the show
                    show (string): number of the show
                    season_padding (int): season padding to be used
                    episode_padding (int): episode padding to be used

            Returns:
            string: full file name with extension
    """
    show_name = name
    season_number = None
    episode_number = None
    episode_name = None
    extension = None
    _, extension = os.path.splitext(filename)

    if show == 2 or show == 3:
        pattern = re.compile(r'\d+x\d+')  # looking for formats like 9x01
        m = re.search(pattern, filename)

        if m:
            season_number = (m.group(0).split('x')[0]).lstrip('0')
            episode_number = (m.group(0).split('x')[1]).lstrip('0')
        if show == 2:
            episode_name = re.split('.WEB', filename)[  # finding the episode name
                0].split(' - ')[-1].strip()
        elif show == 3:
            episode_name = re.split('.HDTV', filename)[  # finding the episode name
                0].split(' - ')[-1].strip()

    else:
        pattern = re.compile(
            "s\d{1,3}e\d{1,3}", re.IGNORECASE)  # looking for formats like s01e02

        m = re.search(pattern, filename)
        if m:
            var = str(m.group(0))
            words = re.split("E", var, flags=re.IGNORECASE)
            # print(words)
            season_number = words[0][1:].lstrip('0')
            episode_number = words[1].lstrip('0')
        episode_name = ""  # no name of episode for Breaking bad

    file = get_episode_name(show_name, season_number, episode_number,
                            episode_name, season_padding, episode_padding)
    file.strip()
    file += extension

    return file


def rename(showname, show, season_padding, episode_padding):
    """This method iterates over all files in wrong_srt folder for a specific tv show

    Args:
            showname (string): name of the tv show to rename
            show (int): number of the show to rename
            season_padding (int): season padding to be used
            episode_padding (int): episode padding to be used
    """
    SHOW_PATH = os.path.join(WRONG_PATH, showname)
    NEW_PATH = os.path.join(CORRECT_PATH, showname)

    # if the folder for the current tv show does not exist, create it
    if not os.path.isdir(NEW_PATH):
        os.mkdir(NEW_PATH)

    # iterating over all files in the tv show's directory
    for filename in os.listdir(SHOW_PATH):
        f = os.path.join(SHOW_PATH, filename)
        # checking if it is a file
        if os.path.isfile(f):
            src = f  # current file is the source
            dst = get_filename(f, showname, show,  # the new file with the corrected name
                               season_padding, episode_padding)
            dst = os.path.join(NEW_PATH, dst)
            print(dst)
            shutil.copy(src, dst)  # copying files to the correct_srt folder


def setup_directories():
    if not os.path.isdir(os.path.join(CWD, CORRECT_PATH)):
        os.mkdir(os.path.join(CWD, CORRECT_PATH))


def regex_renamer():
    """
            This is the driver method that interacts with the user to take in the show number
            , season padding and episode padding.
    """
    # Taking input from the user
    setup_directories()

    print("1. Breaking Bad")
    print("2. Game of Thrones")
    print("3. Lucifer")

    webseries_num = int(
        input("Enter the number of the web series that you wish to rename. 1/2/3: "))
    season_padding = int(input("Enter the Season Number Padding: "))
    episode_padding = int(input("Enter the Episode Number Padding: "))

    name = None

    if webseries_num == 1:
        name = 'Breaking Bad'
    elif webseries_num == 2:
        name = 'Game of Thrones'
    elif webseries_num == 3:
        name = 'Lucifer'
    else:
        print("Invalid season number")
        return

    rename(name, webseries_num, season_padding, episode_padding)


regex_renamer()
