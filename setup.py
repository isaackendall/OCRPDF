from pathlib import Path
from setuptools import setup, find_packages

# Read the contents of README.md
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding="utf-8")

# Define project metadata
NAME = "pdf-ocr-gui"
VERSION = "1.1.0"
DESCRIPTION = "A user-friendly GUI application for performing OCR on PDF files using ocrmypdf"
AUTHOR = "Isaac Kendall"
AUTHOR_EMAIL = "your.email@example.com"
URL = "https://github.com/isaackendall/OCRPDF"
LICENSE = "MIT"

# Define project dependencies
INSTALL_REQUIRES = [
    "ocrmypdf>=14.0.0,<15.0.0",  # OCR functionality
    "pillow>=10.0.0,<11.0.0",     # Image processing
    "tqdm>=4.65.0,<5.0.0",       # Progress bars
]

# Development dependencies
EXTRAS_REQUIRE = {
    "dev": [
        "pytest>=7.0.0,<8.0.0",
        "pytest-cov>=4.0.0,<5.0.0",
        "black>=23.0.0,<24.0.0",
        "isort>=5.12.0,<6.0.0",
        "mypy>=1.0.0,<2.0.0",
        "flake8>=6.0.0,<7.0.0",
    ],
    "build": [
        "pyinstaller>=5.0.0,<6.0.0",
        "setuptools>=65.0.0,<66.0.0",
        "wheel>=0.38.0,<0.39.0",
    ]
}

# Define package data
PACKAGE_DATA = {
    "": ["*.md", "*.txt", "*.json"],
}

# Define entry points
ENTRY_POINTS = {
    "gui_scripts": [
        "pdf-ocr-gui=ocr_gui:main",
    ],
    "console_scripts": [
        "pdf-ocr-cli=ocr_gui:main",
    ],
}

# Define project classifiers
CLASSIFIERS = [
    # Development Status
    "Development Status :: 5 - Production/Stable",
    
    # Intended Audience
    "Intended Audience :: End Users/Desktop",
    "Intended Audience :: Education",
    "Intended Audience :: Legal Industry",
    
    # License
    "License :: OSI Approved :: MIT License",
    
    # Operating System
    "Operating System :: OS Independent",
    "Operating System :: MacOS :: MacOS X",
    "Operating System :: Microsoft :: Windows",
    "Operating System :: POSIX :: Linux",
    
    # Programming Language
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.7",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3 :: Only",
    
    # Topic
    "Topic :: Multimedia :: Graphics :: Graphics Conversion",
    "Topic :: Office/Business",
    "Topic :: Text Processing :: Filters",
    "Topic :: Utilities",
]

# Project URLs
PROJECT_URLS = {
    "Bug Reports": f"{URL}/issues",
    "Documentation": "https://github.com/isaackendall/OCRPDF#readme",
    "Source": URL,
    "Changelog": f"{URL}/releases",
}

setup(
    name=NAME,
    version=VERSION,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type="text/markdown",
    url=URL,
    license=LICENSE,
    
    # Package configuration
    packages=find_packages(exclude=["tests", "tests.*"]),
    package_data=PACKAGE_DATA,
    include_package_data=True,
    zip_safe=False,
    
    # Dependencies
    python_requires=">=3.7",
    install_requires=INSTALL_REQUIRES,
    extras_require=EXTRAS_REQUIRE,
    
    # Entry points
    entry_points=ENTRY_POINTS,
    
    # Metadata
    classifiers=CLASSIFIERS,
    project_urls=PROJECT_URLS,
    keywords="pdf ocr gui ocrmypdf tesseract document text-recognition",
    
    # Additional metadata
    platforms=["any"],
    download_url=f"{URL}/archive/v{VERSION}.tar.gz",
)