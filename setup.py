# flake8: noqa
if __name__ == "__main__":

    """
    This is a setup.py script generated by py2applet
    Usage:
        python setup.py py2app
    """

    from setuptools import setup, find_packages
    from shutil import copyfile
    import os
    import sys
    import re

    # 再帰回数に引っかかるのでとりあえず大きい数に．
    sys.setrecursionlimit(10**9)

    # ------------------------ ここを変更 --------------------------------
    PACKAGE_NAME = "ternary_diagram"  # フォルダの名前も統一
    DESCRIPTION = "This package makes it easier for you to draw beautiful ternary diagram without pymatgen."

    # py2app用の変数
    SRC = ["main.py"]
    DATA_FILES = ["LICENSE"]
    PKGS = []
    ICON = os.path.join("icon", "{}.icns".format(PACKAGE_NAME))
    # --------------------------------------------------------------------

    VERSION_PYTHON = "{0}.{1}".format(
        sys.version_info.major, sys.version_info.minor
    )

    # __init__.pyから読み込む
    with open(
        os.path.join(PACKAGE_NAME, "__init__.py"), encoding="utf-8"
    ) as f:
        init_text = f.read()
        VERSION = re.search(
            r"__version__\s*=\s*[\'\"](.+?)[\'\"]", init_text
        ).group(1)
        LICENSE = re.search(
            r"__license__\s*=\s*[\'\"](.+?)[\'\"]", init_text
        ).group(1)
        AUTHOR = re.search(
            r"__author__\s*=\s*[\'\"](.+?)[\'\"]", init_text
        ).group(1)
        EMAIL = re.search(
            r"__author_email__\s*=\s*[\'\"](.+?)[\'\"]", init_text
        ).group(1)
        ID = re.search(
            r"__user_id__\s*=\s*[\'\"](.+?)[\'\"]", init_text
        ).group(1)
        APP_NAME = re.search(
            r"__app_name__\s*=\s*[\'\"](.+?)[\'\"]", init_text
        ).group(1)
        url = re.search(r"__url__\s*=\s*[\'\"](.+?)[\'\"]", init_text).group(1)

    assert VERSION
    assert LICENSE
    assert AUTHOR
    assert EMAIL
    assert ID
    assert APP_NAME
    assert url

    """
    メモ
    /.pyenv/versions/anaconda3-2019.03/envs/pymat/lib/python3.7/site-packages/PyQt5/uic/port_v2/ascii_upper.pyの28行目を書き換えた．
    少なくともpython3.7においてstringオブジェクトはmaketrans関数を持っておらず，正しくはstr.maketransである．
    python3.8で以前やったときはこのエラーがでなかった．
    * 3.8にアップデートしてやってみる．
        → 3.8だとsetupのほうがエラー起きるので3.6でやってみる．
        3.6は起動後に関数が呼び出せないと言われる
    setup.pyに関する参考サイト
    * https://packaging.python.org/guides/distributing-packages-using-setuptools/#packages
    py2app 0.23や0.22では動作確認
    """

    if "py2app" in sys.argv:
        alias = "-A" in sys.argv or "--alias" in sys.argv

        # 諸変数・定数の定義
        lib_path = os.path.join(os.environ["CONDA_PREFIX"], "lib")
        fname_libpython = "libpython{}.dylib".format(VERSION_PYTHON)

        # libpython3.7.m.dylibだとエラーになるのであらかじめコピーしておく．
        path_original = os.path.join(
            lib_path, "libpython{}m.dylib".format(VERSION_PYTHON)
        )
        path_converted = os.path.join(lib_path, fname_libpython)
        if os.path.exists(path_original) and not os.path.exists(
            path_converted
        ):
            copyfile(path_original, path_converted)

        # 諸変数の準備
        dylib_files = [
            os.path.join(lib_path, f)
            for f in os.listdir(lib_path)
            if ".dylib" in f
        ]
        contents_path = os.path.join(
            "dist", "{}.app".format(APP_NAME), "Contents"
        )
        frameworks_path = os.path.join(contents_path, "Frameworks")

        OPTIONS = {
            "argv_emulation": False,
            "packages": PKGS,
            "iconfile": ICON,
            "plist": {
                "PyRuntimeLocations": [
                    "@executable_path/../Frameworks/{}".format(
                        fname_libpython
                    ),
                    os.path.join(lib_path, fname_libpython),
                ],
                "CFBundleName": APP_NAME,
                "CFBundleDisplayName": APP_NAME,
                "CFBundleGetInfoString": DESCRIPTION,
                "CFBundleIdentifier": "com.{0}.osx.{1}".format(ID, APP_NAME),
                "CFBundleVersion": VERSION,
                "CFBundleShortVersionString": VERSION,
                "NSHumanReadableCopyright": "Copyright © 2021-, {}".format(
                    AUTHOR
                ),
            },
            # 'frameworks': dylib_files,
        }

        setup(
            name=APP_NAME,
            app=SRC,
            author=AUTHOR,
            author_email=EMAIL,
            version=VERSION,
            data_files=DATA_FILES,
            options={"py2app": OPTIONS},
            setup_requires=["py2app"],
            url="https://github.com/{0}/{1}".format(ID, APP_NAME),
        )

        # aliasモードじゃないとき．
        # if not alias:
        #     {copyfile(f, os.path.join(frameworks_path, os.path.basename(f))) for f in dylib_files}
    else:
        """
        参考: https://python-packaging-user-guide-ja.readthedocs.io/ja/latest/distributing.html#manifest-in
        """
        with open("requirements.txt", encoding="utf-8") as requirements_file:
            install_requirements = requirements_file.read().splitlines()

        try:
            with open("README.md", encoding="utf-8") as f:
                long_description = f.read()
        except IOError:
            long_description = ""

        setup(
            name=APP_NAME,
            version=VERSION,
            description=DESCRIPTION,
            long_description=long_description,
            # long_descriptionの形式
            # 'text/plain', 'text/x-rst', 'text/markdown'のいずれかから指定．
            long_description_content_type="text/markdown",
            author=AUTHOR,
            author_email=EMAIL,
            maintainer=AUTHOR,
            maintainer_email=EMAIL,
            install_requires=install_requirements,
            url=url,
            project_urls={
                "Documentation": "https://yu9824.github.io/ternary_diagram/",
                "Source": url,
                "Tracker": "{}/issues".format(url),
                "PyPI": "https://pypi.org/project/ternary-diagram/",
            },  # プロジェクトのホームページやソースコードを置いているリポジトリのURLを指定．
            # PyPIでの検索用キーワードをスペース区切りで指定．
            keywords="ternarydiagram phasediagram chemistry",
            license=LICENSE,
            packages=find_packages(exclude=["example"]),
            classifiers=[
                "License :: OSI Approved :: MIT License",
                "Programming Language :: Python :: 3",
                "Programming Language :: Python :: 3.7",
                "Programming Language :: Python :: 3.8",
                "Programming Language :: Python :: 3.9",
                "Programming Language :: Python :: 3.10",
                "Programming Language :: Python :: 3.11",
                "Topic :: Scientific/Engineering :: Chemistry",
                "Topic :: Scientific/Engineering :: Visualization",
            ],  # パッケージ(プロジェクト)の分類．https://pypi.org/classifiers/ に掲載されているものを指定可能．
        )
