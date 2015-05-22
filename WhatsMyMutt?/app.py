import os
import time
import cPickle
import datetime
import logging
import flask
import werkzeug
import optparse
import tornado.wsgi
import tornado.httpserver
import numpy as np
import pandas as pd
from PIL import Image
import cStringIO as StringIO
import urllib
import exifutil
import re
import caffe
import csv

REPO_DIRNAME = os.path.abspath(os.path.dirname(__file__) + '/../..')
UPLOAD_FOLDER = '/tmp/caffe_demos_uploads'
ALLOWED_IMAGE_EXTENSIONS = set(['png', 'bmp', 'jpg', 'jpe', 'jpeg', 'gif'])

# Obtain the flask app object
app = flask.Flask(__name__)

#image support
reader = csv.reader(open("./examples/web_demo/dogimgs150.csv"))
dogs={}
for row in reader:
  dogs[row[0].lower() ]=row[0:]

dogPattern = ".*(shih-tzu|lhasa|doberman|dandi dinmont|terrier|chinese imperial dog|polish hunting dog|pungsan dog|seppala siberian sleddog|moscow watchdog|seskar seal dog|tahtlan bear dog|tamaskan dog|thai bangkaew dog|bulldog|heading dog|inuit dog|wolfdog|swedish farmdog|cordoba fighting dog|hound|gampr|eskimo dog|cattle dog|barkharwal dog|gaddi dog|greenland dog|hare indian dog|mountain dog|canaan dog|bull|vizsla|pembroke|kelpie|griffon|malamute|pug|akita|whippet|retriever|poodle|beagle|dalmatian|husky|spaniel|weimaraner|wetterhoun|ridgeback|mastiff|tornjak|taigan|talbot|telomian|cimarron|villano|volpino|bracke|tosa|brindle|saluki|sapsali|sarplaninac|segugio|kopov|smalandsstovare|samoyed|schapendoes|schipperke|shiba inu|shih tzu|shikoku|sloughi|cuvac|poi dog|pariah dog|kangal dog|karakachan dog|karelian bear dog|hairless dog|water dog|pointer|spinone italiano|bernard|stabyhoun|schnauzer|hund|sabueso|rajapalayam|brasileiro|ratonero|tracker|laika|rafeiro do alentejo|rottweiler|russian toy|papillon|pekingese|corgi|pachon navarro|pandikona|perro|phalene|podenco|poitevin|porcelaine|Prazsky Krysarik|peruvian inca orchid|plott|pomeranian|podengo|puli|pumi|shepherd|newfoundland|norbottenspets|maltese|pinscher|magyar agar|mcnab|mioritic|molossus|cur|mucuchies|munsterlander|mudi|lagotto romagnolo|heeler|leonberger|leonberg|lhasa apso|lowchen|kaikadi|kai ken|kanni|hond|kintamani|kishu ken|komondor|kromfohrlander|kuri|kuvasz|kyi-leo|chin|jindo|setter|hamiltonstovare|harrier|havanese|herder|hovawart|spitz|great dane|pyrenees|eurasier|dogo|bordeaux|corso|ovcharka|chihuahua|chinese crested|chongqing|shar-pei|chinook|chow|cirneco dell'etna|collie|vlcak|barbet|basenji|beauceron|laekenois|malinois|tervuren|bichon|boerboel|bolognese|borzoi|bouvier|boxer|brace italiano|braque|briard|brittany|ratter|basset|berger|billy|bleu de gascogne|lacy|bullenbeisser|bully kutta|cao|cesky|chien|chippiparai|cierny sery|combai|coton de tulear|cursinu|broholmer|appenzeller sennenhunde|azawakh|xoloitzcuintli|aidi|akbash|klee kai|alano|ariegeois|armant|drever|drunker|elo|picardie|gascon|hokkaido ken|huntaway|koolie).*"

p = re.compile(dogPattern, re.I)

@app.route('/')
def index():
    return flask.render_template('index.html', has_result=False)


@app.route('/classify_url', methods=['GET'])
def classify_url():
    imageurl = flask.request.args.get('imageurl', '')
    try:
        string_buffer = StringIO.StringIO(
            urllib.urlopen(imageurl).read())
        image = caffe.io.load_image(string_buffer)

    except Exception as err:
        # For any exception we encounter in reading the image, we will just
        # not continue.
        logging.info('URL Image open error: %s', err)
        return flask.render_template(
            'index.html', has_result=True,
            result=(False, 'Cannot open image from URL.')
        )

    logging.info('Image: %s', imageurl)
    result = app.clf.classify_image(image)
    return flask.render_template(
        'index.html', has_result=True, result=result, imagesrc=imageurl)


@app.route('/classify_upload', methods=['POST'])
def classify_upload():
    try:
        logging.info('in classify_upload')
        # We will save the file to disk for possible data collection.
        imagefile = flask.request.files['imagefile']
        logging.info('in classify_upload 1')
        filename_ = str(datetime.datetime.now()).replace(' ', '_') + \
            werkzeug.secure_filename(imagefile.filename)
        logging.info('in classify_upload 2')
        filename = os.path.join(UPLOAD_FOLDER, filename_)
        logging.info('in classify_upload 3')
        imagefile.save(filename)
        logging.info('Saving to %s.', filename)
        image = exifutil.open_oriented_im(filename)

    except Exception as err:
        logging.info('Uploaded image open error: %s', err)
        return flask.render_template(
            'index.html', has_result=True,
            result=(False, 'Cannot open uploaded image.')
        )

    result = app.clf.classify_image(image)
    return flask.render_template(
        'index.html', has_result=True, result=result,
        imagesrc=embed_image_html(image)
    )

#posts results for All my Results tab.
@app.route('/myclassify_upload', methods=['POST'])
def myclassify_upload():
    try:
        logging.info('in classify_upload')
        # We will save the file to disk for possible data collection.
        imagefile = flask.request.files['imagefile']
        logging.info('in classify_upload 1')
        filename_ = str(datetime.datetime.now()).replace(' ', '_') + \
            werkzeug.secure_filename(imagefile.filename)
        logging.info('in classify_upload 2')
        filename = os.path.join(UPLOAD_FOLDER, filename_)
        logging.info('in classify_upload 3')
        imagefile.save(filename)
        logging.info('Saving to %s.', filename)
        image = exifutil.open_oriented_im(filename)

    except Exception as err:
        logging.info('Uploaded image open error: %s', err)
        return flask.render_template(
            'response.html', has_result=True,
            result=(False, 'Cannot open uploaded image.')
        )

    result = app.clf.classify_image(image)
    return flask.render_template(
        'response.html', has_result=True, result=result,
        imagesrc=embed_image_html(image)
    )

#posts results for Dogs Only tab.
@app.route('/myclassify_dog_upload', methods=['POST'])
def myclassify_dog_upload():
    try:
        logging.info('in classify_upload')
        # We will save the file to disk for possible data collection.
        imagefile = flask.request.files['imagefile']
        logging.info('in classify_upload 1')
        filename_ = str(datetime.datetime.now()).replace(' ', '_') + \
            werkzeug.secure_filename(imagefile.filename)
        logging.info('in classify_upload 2')
        filename = os.path.join(UPLOAD_FOLDER, filename_)
        logging.info('in classify_upload 3')
        imagefile.save(filename)
        logging.info('Saving to %s.', filename)
        image = exifutil.open_oriented_im(filename)

    except Exception as err:
        logging.info('Uploaded image open error: %s', err)
        return flask.render_template(
            'responseDogs.html', has_result=True,
            result=(False, 'Cannot open uploaded image.')
        )

    result = app.clf.classify_image(image)
    i = 0
    while i < len(result[1]):
         single_pred = result[1][i]
         if not(p.match(single_pred[0])):
           logging.info(single_pred[0] + " i=" + str(i))
           del result[1][i]
         else:
           #image support
           searchre = re.compile('.*'+single_pred[0].lower()+'.*',re.IGNORECASE)
           defkey = "borzoi"
           for key in dogs:
             if searchre.match(key):
               defkey = key
               break
           result[1][i] = [ single_pred[0], single_pred[1], dogs[defkey][2]]
           '''
           if single_pred[0].lower() in dogs:
             result[1][i] = [ single_pred[0], single_pred[1], dogs[single_pred[0].lower()][2]]
           else: 
             result[1][i] = [ single_pred[0], single_pred[1], dogs["borzoi"][2]]
           '''
           i = i + 1
 
    return flask.render_template(
        'responseDogs.html', has_result=True, result=result,
        imagesrc=embed_image_html(image)
    )

def embed_image_html(image):
    """Creates an image embedded in HTML base64 format."""
    image_pil = Image.fromarray((255 * image).astype('uint8'))
    image_pil = image_pil.resize((256, 256))
    string_buf = StringIO.StringIO()
    image_pil.save(string_buf, format='png')
    data = string_buf.getvalue().encode('base64').replace('\n', '')
    return 'data:image/png;base64,' + data

def allowed_file(filename):
    return (
        '.' in filename and
        filename.rsplit('.', 1)[1] in ALLOWED_IMAGE_EXTENSIONS
    )


class ImagenetClassifier(object):
    default_args = {
        'model_def_file': (
            '{}/models/bvlc_reference_caffenet/deploy.prototxt'.format(REPO_DIRNAME)),
        'pretrained_model_file': (
            '{}/models/bvlc_reference_caffenet/bvlc_reference_caffenet.caffemodel'.format(REPO_DIRNAME)),
        'mean_file': (
            '{}/python/caffe/imagenet/ilsvrc_2012_mean.npy'.format(REPO_DIRNAME)),
        'class_labels_file': (
            '{}/data/ilsvrc12/synset_words.txt'.format(REPO_DIRNAME)),
        'bet_file': (
            '{}/data/ilsvrc12/imagenet.bet.pickle'.format(REPO_DIRNAME)),
    }
    for key, val in default_args.iteritems():
        if not os.path.exists(val):
            raise Exception(
                "File for {} is missing. Should be at: {}".format(key, val))
    default_args['image_dim'] = 256
    default_args['raw_scale'] = 255.

    def __init__(self, model_def_file, pretrained_model_file, mean_file,
                 raw_scale, class_labels_file, bet_file, image_dim, gpu_mode):
        logging.info('Loading net and associated files...')
        if gpu_mode:
            caffe.set_mode_gpu()
        else:
            caffe.set_mode_cpu()
        self.net = caffe.Classifier(
            model_def_file, pretrained_model_file,
            image_dims=(image_dim, image_dim), raw_scale=raw_scale,
            mean=np.load(mean_file).mean(1).mean(1), channel_swap=(2, 1, 0)
        )

        with open(class_labels_file) as f:
            labels_df = pd.DataFrame([
                {
                    'synset_id': l.strip().split(' ')[0],
                    'name': ' '.join(l.strip().split(' ')[1:]).split(',')[0]
                }
                for l in f.readlines()
            ])
        self.labels = labels_df.sort('synset_id')['name'].values

        self.bet = cPickle.load(open(bet_file))
        # A bias to prefer children nodes in single-chain paths
        # I am setting the value to 0.1 as a quick, simple model.
        # We could use better psychological models here...
        self.bet['infogain'] -= np.array(self.bet['preferences']) * 0.1

    def classify_image(self, image):
        try:
            starttime = time.time()
            scores = self.net.predict([image], oversample=True).flatten()
            endtime = time.time()

            indices = (-scores).argsort()[:5]
            predictions = self.labels[indices]

            # In addition to the prediction text, we will also produce
            # the length for the progress bar visualization.
            meta = [
                (p, '%.5f' % scores[i])
                for i, p in zip(indices, predictions)
            ]
            logging.info('result: %s', str(meta))

            # Compute expected information gain
            expected_infogain = np.dot(
                self.bet['probmat'], scores[self.bet['idmapping']])
            expected_infogain *= self.bet['infogain']

            # sort the scores
            infogain_sort = expected_infogain.argsort()[::-1]
            bet_result = [(self.bet['words'][v], '%.5f' % expected_infogain[v])
                          for v in infogain_sort[:5]]
            logging.info('bet result: %s', str(bet_result))

            return (True, meta, bet_result, '%.3f' % (endtime - starttime))

        except Exception as err:
            logging.info('Classification error: %s', err)
            return (False, 'Something went wrong when classifying the '
                           'image. Maybe try another one?')


def start_tornado(app, port=5000):
    http_server = tornado.httpserver.HTTPServer(
        tornado.wsgi.WSGIContainer(app))
    http_server.listen(port)
    print("Tornado server starting on port {}".format(port))
    tornado.ioloop.IOLoop.instance().start()


def start_from_terminal(app):
    """
    Parse command line options and start the server.
    """
    parser = optparse.OptionParser()
    parser.add_option(
        '-d', '--debug',
        help="enable debug mode",
        action="store_true", default=False)
    parser.add_option(
        '-p', '--port',
        help="which port to serve content on",
        type='int', default=5000)
    parser.add_option(
        '-g', '--gpu',
        help="use gpu mode",
        action='store_true', default=False)

    opts, args = parser.parse_args()
    ImagenetClassifier.default_args.update({'gpu_mode': opts.gpu})

    # Initialize classifier + warm start by forward for allocation
    app.clf = ImagenetClassifier(**ImagenetClassifier.default_args)
    app.clf.net.forward()

    if opts.debug:
        app.run(debug=True, host='0.0.0.0', port=opts.port)
    else:
        start_tornado(app, opts.port)


if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    start_from_terminal(app)
