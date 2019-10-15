import imageio
from datetime import date, timedelta
import h5py as h5
import plotgenNeat

MIN_TIMESTEP = '00'
MAX_TIMESTEP = '07'
H5_DIRECTORY = '/global/cscratch1/sd/amahesh/gb_data/All-Hist/'

# https://stackoverflow.com/questions/753190/programmatically-generate-video-or-animated-gif-in-python
# TODO: error handling for when there are not images ahead or behind
def create_gif(filename, save_location, num_timesteps=24, delay=0.5):
    """
    Save a gif to save_location, with each frame corresponding to an image file path specified with filenames. Delay
    specifies the amount of time before switching between frames.
    """
    filenames = prev_timesteps(filename, num_timesteps) + [filename] + next_timesteps(filename, num_timesteps)
    map(lambda filename: H5_DIRECTORY + filename, filenames)
    images = get_TMQ_fields(filenames)

    with imageio.get_writer(save_location, mode='I', duration=delay) as writer:
        for image in images:
            writer.append_data(image)

def get_TMQ_fields(filenames):
    """
    :param filenames: a list of filenames for the h5 files to extract the TMQ field from
    :return: a list corresponding to the TMQ numpy array for each filename in filenames
    """
    result = []

    for filename in filenames:
        h5_file = h5.File(filename)
        TMQ = h5_file['climate']['data'][:, :, 0]
        result.append(plotgenNeat.process_tmq_field(TMQ, land=False))

    return result

# assumes that filename is properly formatted in the form data-year-month-day-timestep-run
def next_timesteps(filename, num_steps):
    result = []
    current_filename = filename
    for i in range(num_steps):
        current_filename = add_timestep(current_filename)
        result.append(current_filename)

    return result

def prev_timesteps(filename, num_steps):
    result = []
    current_filename = filename
    for i in range(num_steps):
        current_filename = minus_timestep(current_filename)
        result.append(current_filename)

    return result

# returns the filename corresponding to a single forward timestep
def add_timestep(filename):
    filename_split = filename.split('-')
    timestep = int(filename_split[4])
    if timestep < 7:
        filename_split[4] = '0' + str(timestep + 1)
        return '-'.join(filename_split)
    else:
        current_date = date(int(filename_split[1]), int(filename_split[2]), int(filename_split[3]))
        day_delta = timedelta(days=1)
        return filename_split[0] + '-' + str(current_date + day_delta) + '-' + MIN_TIMESTEP + '-' + filename_split[5]

# returns the filename corresponding to a single backwards timestep
def minus_timestep(filename):
    filename_split = filename.split('-')
    timestep = int(filename_split[4])
    if timestep > 0:
        filename_split[4] = '0' + str(timestep - 1)
        return '-'.join(filename_split)
    else:
        current_date = date(int(filename_split[1]), int(filename_split[2]), int(filename_split[3]))
        day_delta = timedelta(days=1)
        return filename_split[0] + '-' + str(current_date - day_delta) + '-' + MAX_TIMESTEP + '-' + filename_split[5]
