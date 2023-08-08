from setuptools import setup

setup(
    name='sasta-skit',
    version = '1.0',
    author = 'Harikrishna Pillai',
    author_email = 'hari3032003@gmail.com',
    url = 'https://github.com/Harikrishna-AL/sasta-skit',
    packages = ['sasta_skit'],
    install_requires = [
        'streamlit',
        'openai',
        'transformers',
        'soundfile',
        'librosa',
        'audio_recorder_streamlit',
        'datasets',
        'python-dotenv',
    ],
    classifiers = [
        'Development Status :: 1 - Planning',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License', 
        'Programming Language :: Python :: 3.7',
    ],
)
