# What is This?
This is a Python script utilising the pillow library for mass-manipulating image files in a given directory and sub-directories, and saving them in a separate location. Although it was made with Eastside Hockey Manager in mind, it can technically be used with any application that has a similar approach to displaying graphics, thanks to the customisability of the script behaviour.
# How to Install
## Windows
- [Download](https://github.com/saileille/ehm-graphics-tool/releases/latest) the `main.exe` file.
- [Download](https://github.com/saileille/ehm-graphics-tool/blob/master/settings.json) the `settings.json` file, and place it in the same directory as `main.exe`.
## Not-Windows
- [Download](https://github.com/saileille/ehm-graphics-tool/archive/refs/heads/master.zip) the entire master branch and extract it to the location of your liking.
- [Install](https://www.python.org/downloads/) Python 3.
- [Install](https://pypi.org/project/pillow/) pillow.
- To run the script, execute the `main.py` file, located at the root of the project directory.
# How to Use
Before using the script, you need to give it instructions on what you want to do. [_config.json](https://github.com/saileille/ehm-graphics-tool/blob/master/docs/_config.json) and [settings.json](https://github.com/saileille/ehm-graphics-tool/blob/master/docs/settings.json), located in the project's `docs` directory, have all the technical documentation you need, while this guide attempts to teach you how to use those files with practical examples.
## Configuring the `settings.json` File
The [settings.json](https://github.com/saileille/ehm-graphics-tool/blob/master/settings.json) file in the project's root directory has ready-made instructions to get you started, but you need to at least change `graphics_folder` and `source_folder` to the game's graphics folder location and the folder location of your source images, respectively.

Inside `settings.json`:
```json
"graphics_folder": "D:/SteamLibrary/steamapps/common/Eastside Hockey Manager/data/pictures <-- If your game is located in a different folder, you must change this.",
"source_folder": "E:/Files/EHM Graphics Project <-- Change this to the folder where you keep your source images.",
...
```
On Windows, you can use either slash (`/`) or two backslashes (`\\`) to separate folders from one another. This applies to every setting in both `settings.json` and `_config.json`.

## Templates
The default `settings.json` file is made to be as simple as possible, but if you want to customise the instructions to your liking, I recommend using templates. Templates allow for quicker and easier changes in the `settings.json` file, useful particularly if you are testing how different configurations work in the game. For example, backgrounds in the default `settings.json` file are defined like so:
```json
"backgrounds/awards": {
    "width": 1024,
    "height": 768,
    "trim": true,
    "extension": "jpg",
    "padding_top": 128
},
"backgrounds/clubs/{folder}": {
    "width": 1024,
    "height": 768,
    "trim": true,
    "extension": "jpg",
    "padding_top": 128
},
"backgrounds/comps": {
    "width": 1024,
    "height": 768,
    "trim": true,
    "extension": "jpg",
    "padding_top": 128
},
"backgrounds/nations/{folder}": {
    "width": 1024,
    "height": 768,
    "trim": true,
    "extension": "jpg",
    "padding_top": 128
},
"backgrounds/nonplayers": {
    "width": 1024,
    "height": 768,
    "trim": true,
    "extension": "jpg",
    "padding_top": 128
},
"backgrounds/players": {
    "width": 1024,
    "height": 768,
    "trim": true,
    "extension": "jpg",
    "padding_top": 128
},
...
```
It is unlikely that we will ever find ourselves in a situation where instructions for these folders would differ. It thus makes sense to create a template to define a behaviour, and call that template for each of the folders.

Inside `settings.json`, create a new section called `templates`, and make a new entry called `background_image` inside it, holding the same instructions as the background folders.
```json
{
    "graphics_folder": "D:/SteamLibrary/steamapps/common/Eastside Hockey Manager/data/pictures",
	"source_folder": "E:/Files/EHM Graphics Project",
    "templates": {
        "background_image": {
			"width": 1024,
			"height": 768,
			"trim": true,
			"extension": "jpg",
			"padding_top": 128
        }
    },
	"instructions": {
		"backgrounds/awards": {
			"width": 1024,
			"height": 768,
			"trim": true,
			"extension": "jpg",
			"padding_top": 128
		},
		"backgrounds/clubs/{folder}": {
			"width": 1024,
			"height": 768,
			"trim": true,
			"extension": "jpg",
			"padding_top": 128
		},
        ...
    }
}
```
Then, define each background folder instruction with that template name (`background_image`):
```json
{
    "graphics_folder": "D:/SteamLibrary/steamapps/common/Eastside Hockey Manager/data/pictures",
	"source_folder": "E:/Files/EHM Graphics Project",
    "templates": {
        "background_image": {
			"width": 1024,
			"height": 768,
			"trim": true,
			"extension": "jpg",
			"padding_top": 128
        }
    },
	"instructions": {
		"backgrounds/awards": "background_image",
		"backgrounds/clubs/{folder}": "background_image",
		"backgrounds/comps": "background_image",
		"backgrounds/nations/{folder}": "background_image",
		"backgrounds/nonplayers": "background_image",
		"backgrounds/players": "background_image",
        ...
    }
}
```
If you define a folder's image processing behaviour with a template name, that template obviously has to exist in the `templates` section. However, a template can be left unused, and the script does not complain. Eastside Hockey Manager comes with many resolutions, and each of those resolutions requires a differently sized background image. We can quickly and easily build background images of different sizes by defining several background templates, and then calling the one we want to use.
```json
{
    "graphics_folder": "D:/SteamLibrary/steamapps/common/Eastside Hockey Manager/data/pictures",
	"source_folder": "E:/Files/EHM Graphics Project",
    "templates": {
        "background_image_1024x768": {
			"width": 1024,
			"height": 768,
			"trim": true,
			"extension": "jpg",
			"padding_top": 128
        },
        "background_image_1280x768": {
			"width": 1280,
			"height": 768,
			"trim": true,
			"extension": "jpg",
			"padding_top": 128
        },
        "background_image_1366x768": {
			"width": 1366,
			"height": 768,
			"trim": true,
			"extension": "jpg",
			"padding_top": 128
        },
        "background_image_1440x900": {
			"width": 1440,
			"height": 900,
			"trim": true,
			"extension": "jpg",
			"padding_top": 128
        },
        "background_image_1980x1080": {
			"width": 1980,
			"height": 1080,
			"trim": true,
			"extension": "jpg",
			"padding_top": 128
        }
    },
	"instructions": {
		"backgrounds/awards": "background_image_1024x768",
		"backgrounds/clubs/{folder}": "background_image_1024x768",
		"backgrounds/comps": "background_image_1024x768",
		"backgrounds/nations/{folder}": "background_image_1024x768",
		"backgrounds/nonplayers": "background_image_1024x768",
		"backgrounds/players": "background_image_1024x768",
        ...
    }
}
```
For in-detail documentation of what everything means, see [settings.json](https://github.com/saileille/ehm-graphics-tool/blob/master/docs/settings.json).
## Configuring a Master `_config.json` File
Unlike with `settings.json`, you can have as many `_config.json` files as you like, wherever you want in your source folder. While not obligatory, I recommend creating one at the root of your source folder as a master config file, and that is what we are going to do in this guide.

Let's presume you have the following folder structure in your source directory:
```
source_folder/
├── clubs/
│   ├── backgrounds/
│   └── logos/
├── comps/
│   ├── backgrounds/
│   └── logos/
├── nations/
│   ├── backgrounds/
│   ├── crest logos/
│   ├── hockey country flags/
│   ├── iha logos/
│   └── rest of the world flags/
└── people/
    └── backgrounds/
```
We are going to create a new `_config.json` file at the root of the folder, like so:
```
source_folder/
├── clubs/
│   ├── backgrounds/
│   └── logos/
├── comps/
│   ├── backgrounds/
│   └── logos/
├── nations/
│   ├── backgrounds/
│   ├── crest logos/
│   ├── hockey country flags/
│   ├── iha logos/
│   └── rest of the world flags/
├── people/
│   └── backgrounds/
└── _config.json
```
In that `_config.json`, we write the following instructions:
```json
{
    "clubs/backgrounds/": {
        "override": [
            "backgrounds/clubs/{folder}"
        ]
    },
    "clubs/logos/": {
        "override": [
            "logos/clubs/huge/{folder}",
            "logos/clubs/large/{folder}",
            "logos/clubs/medium/{folder}",
            "logos/clubs/small/{folder}"
        ]
    },
    "comps/backgrounds/": {
        "override": [
            "backgrounds/comps"
        ]
    },
    "comps/logos/": {
        "override": [
            "logos/comps/huge",
            "logos/comps/large",
            "logos/comps/medium",
            "logos/comps/small"
        ]
    },
    "nations/backgrounds/": {
        "override": [
            "backgrounds/nations/{folder}"
        ]
    },
    "nations/hockey country flags/": {
        "override": [
            "logos/nations/small/{folder}"
        ]
    },
    "nations/rest of the world flags/": {
        "override": [
            "logos/nations/huge/{folder}",
            "logos/nations/large/{folder}",
            "logos/nations/medium/{folder}",
            "logos/nations/small/{folder}"
        ]
    },
    "nations/iha logos/": {
        "override": [
            "logos/nations/huge/{folder}"
        ]
    },
    "nations/crest logos/": {
        "override": [
            "logos/nations/large/{folder}",
            "logos/nations/medium/{folder}"
        ]
    },
    "people/backgrounds/": {
        "override": [
            "backgrounds/nonplayers",
            "backgrounds/players"
        ]
    }
}
```
In this configuration, what we do with club and competition logos is pretty straight-forward. We simply instruct the script to take the source image, process it for each logo size according to the instructions defined in `settings.json`, and save them there. With nation logos, it gets more interesting.

We are organising country flags in two folders: `hockey country flags` and `rest of the world flags`. If a country has an ice hockey-related logo (either a team crest or an IHA), its flag gets placed in the `hockey country flags` folder, so only the small version of the flag is saved in the game's graphics folder. If the country is a non-hockey country, its flag is placed in `rest of the world flags`, and the country flag is used for every nation logo size. We are further separating the hockey countries' IHA logos and jersey logos to `iha logos` and `crest logos` folders, respectively. The IHA logos are used in the manager selection screen, while the jersey logos are used everywhere else.

Our configuration does not separate players and non-players. Instead, all people backgrounds are in the same folder, and they get saved as both nonplayers and players.
> [!IMPORTANT]
> All paths used in `override`, `include` and `exclude` settings MUST have defined instructions in `settings.json`!
## Fine-Tuning with Additional `_config.json` Files
A single master configuration file can be sufficient, but there can be cases when you want further customisation. Perhaps the same logo is used by multiple teams or competitions. Maybe you want to use an alternative logo for some teams in some logo sizes. What about adding home and away logos? All this is possible by altering or entirely replacing the master config's behaviour in other config files.
## The `override` and `save_as` Settings
Let's say you have the following files inside `clubs/logos/Finland`:
```
source_folder/
    └── clubs/
        └── logos/
            └── Finland/
                ├── Joensuun Jokipojat HOME-AWAY.png
                └── Joensuun Jokipojat.png
```
With the settings of the `_config.json` we defined in the root directory, we would create a logo in the game's graphics folder that would never be used, as "Joensuun Jokipojat HOME-AWAY" is not a club based in Finland, or anywhere else for that matter. To make the script save these logos the way we want, we are going to create another `_config.json` file in the `Finland` folder, like so:
```
source_folder/
└── clubs/
    └── logos/
        └── Finland/
            ├── _config.json
            ├── Joensuun Jokipojat HOME-AWAY.png
            └── Joensuun Jokipojat.png

```
In the newly created `_config.json` file, we are going to write the following instructions:
```json
{
    "Joensuun Jokipojat HOME-AWAY": {
        "save_as": "Joensuun Jokipojat",
        "override": [
            "logos/clubs/large/{folder}/away",
            "logos/clubs/large/{folder}/home"
        ]
    }
}
```
Here, the `override` setting tells the script that with the image called "Joensuun Jokipojat HOME-AWAY" in this specific folder, all previous instructions are to be disregarded, and that this logo should only be saved in the `logos/clubs/large/Finland/away` and `home` folders. As "Joensuun Jokipojat HOME-AWAY" is still not a real team name, we must also tell the script that the processed images should be saved as "Joensuun Jokipojat" in the game's graphics folders.
> [!NOTE]
> The setting `save_as` cannot be defined for entire folders, only for individual files.
## Fine-Tuning in the Master `_config.json` File
You can refer to any any image, sub-folder, or image of a sub-folder in a `_config.json` file. We could make this configuration in the master `_config.json` file just as well, in which case we should add the following entry to it:
```json
"clubs/logos/Finland/Joensuun Jokipojat HOME-AWAY": {
    "save_as": "Joensuun Jokipojat",
    "override": [
        "logos/clubs/large/{folder}/away",
        "logos/clubs/large/{folder}/home"
    ]
}
```
This method is much more verbose, though, and would soon become a lot of work to manage, so it is better to create new `_config.json` files closer to the folders and files whose behaviour you want to fine-tune.
## The `duplicate` Setting
Let us presume that in the database we are using, the club Joensuun Jokipojat has two junior teams. "Joensuun Jokipojat A-Jrs" and "Joensuun Jokipojat B-Jrs". While we could copy the source image and just create new entries for both of those teams in the `_config.json` file, there is a better alternative - we can tell the script to save the same image more than once. To do that, we must modify the `_config.json` of the `Finland` folder once more:
```json
{
    "Joensuun Jokipojat HOME-AWAY": {
        "save_as": "Joensuun Jokipojat",
        "override": [
            "logos/clubs/large/{folder}/away",
            "logos/clubs/large/{folder}/home"
        ],
        "duplicates": [
            "Joensuun Jokipojat A-Jrs",
            "Joensuun Jokipojat B-Jrs"
        ]
    },
    "Joensuun Jokipojat": {
        "duplicates": [
            "Joensuun Jokipojat A-Jrs",
            "Joensuun Jokipojat B-Jrs"
        ]
    }
}
```
The `duplicates` setting simply tells the script: "Whatever you are doing with this source image, also save it to the same locations with these file names." For this reason, we have to apply the `duplicates` setting to both source images that we use for Joensuun Jokipojat, as the script has no way to understand that "Joensuun Jokipojat HOME-AWAY" and "Joensuun Jokipojat" are connected. This makes writing the `_config.json` file more verbose, but it also allows for more control. For example, if we wanted the junior teams to only use the normal logo of the club, even in matches, we could simply not write the `duplicates` setting for "Joensuun Jokipojat HOME-AWAY".
## The `exclude` Setting
We have created a few more logos, and our `Finland` folder now looks like this:
```
source_folder/
    └── clubs/
        └── logos/
            └── Finland/
                ├── _config.json
                ├── Hameenlinnan Pallokerho ALT.png
                ├── Hameenlinnan Pallokerho.png
                ├── Joensuun Jokipojat HOME-AWAY.png
                └── Joensuun Jokipojat.png
```
We want to use the alternative logo for Hämeenlinnan Pallokerho, which we have named "Hameenlinnan Pallokerho ALT", as the medium-sized logo for the club. It is doable with what we have already learnt adding the following entries to our `_config.json`:
```json
"Hameenlinnan Pallokerho ALT": {
    "save_as": "Hameenlinnan Pallokerho",
    "override": [
        "logos/clubs/medium/{folder}"
    ],
    "duplicates": [
        "Hameenlinnan Pallokerho A-Jrs",
        "Hameenlinnan Pallokerho B-Jrs"
    ]
},
"Hameenlinnan Pallokerho": {
    "override": [
        "logos/clubs/huge/{folder}",
        "logos/clubs/large/{folder}",
        "logos/clubs/small/{folder}"
    ],
    "duplicates": [
        "Hameenlinnan Pallokerho A-Jrs",
        "Hameenlinnan Pallokerho B-Jrs"
    ]
}
```
This method is problematic, though. What if we want to change the default configuration for club logos in the root directory's `_config.json` file in the future? We would have to reflect these changes in every normal image and sub-folder whose behaviour we had overridden up to that point. The less verbose and more easily maintainable way to do it is to use the `exclude` setting:
```json
"Hameenlinnan Pallokerho ALT": {
    "save_as": "Hameenlinnan Pallokerho",
    "override": [
        "logos/clubs/medium/{folder}"
    ],
    "duplicates": [
        "Hameenlinnan Pallokerho A-Jrs",
        "Hameenlinnan Pallokerho B-Jrs"
    ]
},
"Hameenlinnan Pallokerho": {
    "exclude": [
        "logos/clubs/medium/{folder}"
    ],
    "duplicates": [
        "Hameenlinnan Pallokerho A-Jrs",
        "Hameenlinnan Pallokerho B-Jrs"
    ]
}
```
The `exclude` setting tells the script to keep the existing instructions in mind, but to remove the given game graphics folder paths for this particular file or sub-folder. Now, even if we edit other `_config.json` files that affect our `Finland` folder as well, the script behaves as we expect without the need to go through possibly hundreds of folders and `_config.json` files in a hunt for outdated `override`s.
## The `include` Setting
The `include` setting functions the opposite way of `exclude`. Instead of removing things from the script's defined behaviour, it adds to it. Since the behaviour of these two settings is so similar, let's do something more interesting this time. We have once again added logos for a club in our `Finland` folder:
```
source_folder/
└── clubs/
    └── logos/
        └── Finland/
            ├── _config.json
            ├── Hameenlinnan Pallokerho ALT.png
            ├── Hameenlinnan Pallokerho.png
            ├── Helsingin Jokerit HOME-LARGE.png
            ├── Helsingin Jokerit.png
            ├── Joensuun Jokipojat HOME-AWAY.png
            └── Joensuun Jokipojat.png
```
As the image name suggests, we want to use the image "Helsingin Jokerit HOME-LARGE" as the home logo of the club, and the regular large logo. All other logo sizes should be covered by the standard "Helsingin Jokerit" image. The best way to do this is:
```json
"Helsingin Jokerit HOME-LARGE": {
    "save_as": "Helsingin Jokerit",
    "override": [
        "logos/clubs/large/{folder}"
    ],
    "duplicates": [
        "Helsingin Jokerit A-Jrs",
        "Helsingin Jokerit B-Jrs"
    ]
},
"Helsingin Jokerit": {
    "exclude": [
        "logos/clubs/large/{folder}"
    ],
    "include": [
        "logos/clubs/large/{folder}/away"
    ],
    "duplicates": [
        "Helsingin Jokerit A-Jrs",
        "Helsingin Jokerit B-Jrs"
    ]
}
```
As you can see, we can both `include` and `exclude` paths in the same entry!
> [!NOTE]
> You cannot use the `override` setting in the same entry with `include` or `exclude`, as `override` redefines the script's behaviour, while `include` and `exclude` alter it.
## The `ignore` Setting
We have added lots of files to our `Finland` folder, and even made logos that we might want to use at some time in the future. We have decided to put them in a folder called `alternatives`.
```
source_folder/
└── clubs/
    └── logos/
        └── Finland/
            ├── alternatives/
            │   ├── Espoon Blues.png
            │   ├── Heinolan Kiekko.png
            │   └── Helsingin IFK.png
            ├── _config.json
            ├── D-Kiekko Jyvaskyla.png
            ├── Espoon Blues.png
            └── ...
```
We obviously do not want the script to process and save these images, so we are going to tell it to not worry about them. For that, we need to use the `ignore` setting, and instead of using our old `_config.json` file, we are going to create a new one in the `alternatives` folder.
```
source_folder/
└── clubs/
    └── logos/
        └── Finland/
            └── alternatives/
                ├── _config.json
                ├── Espoon Blues.png
                ├── Heinolan Kiekko.png
                └── Helsingin IFK.png
```
Inside, we are going to simply write:
```json
{
    ".": {
        "ignore": true
    }
}
```
> [!TIP]
> The "." refers to the directory where the `_config.json` file is located.

Of course, we can also do this in our `Finland` folder's `_config.json` file, in which case the entry would look like this:
```json
"alternatives/": {
    "ignore": true
}
```
> [!IMPORTANT]
> Note the slash at the end! It is important, as it tells the script that this entry is referring to a folder, not an image.

> [!TIP]
> The script does not stop scanning the sub-folders of a folder that is set to be `ignore`d, so you can un-`ignore` sub-folders or images in a `_config.json` file, just like you can overwrite any other setting.

The rest of the available settings can be found in the [_config.json](https://github.com/saileille/ehm-graphics-tool/blob/master/docs/_config.json) file of the project's `docs` folder.
# Under the Hood
This is a simplified description of what the script does.
1. The script reads every `_config.json` file in the `source_folder` and its sub-folders.
2. The script generates configuration rules for every image in the `source_folder`.
    - The priority hierarchy is, from most important to least important, as follows:
        1. The `_config.json` file locations, starting from the source image location and going up the directory tree.
        2. Entry for the source image in the `_config.json` file.
        3. The `_config.json` folder entries, starting from the source image location and going up the directory tree.
3. The script goes through the source images one by one, processing and saving them.
    - The order of the processing is as follows:
        1. The image is trimmed to the aspect ratio of the required dimensions, if `trim` is set to `true`.
        2. The image is resized to fit the required dimensions.
        3. Transparency is applied, if `opacity` is set to anything but `1.0`.
        4. The mask is applied, if `mask` is set.
        5. Padding is applied, if `padding_top`, `padding_bottom`, `padding_left` or `padding_right` is something else than `0`.
# Version History
## [1.0.2 - Latest](https://github.com/saileille/ehm-graphics-tool/releases/latest)
 - Added templates.
 - The `folder` setting in `_config.json` can now be reset back to its default behaviour by defining it as an empty string (`""`).
 - Replaced the icon of the executable.
 - Added version information to the executable.
## [1.0.1](https://github.com/saileille/ehm-graphics-tool/releases/tag/1.0.1)
- Fixed a bug where the script treated folder configuration as an image if image of the same name existed.
- Made it possible to change the Y-axis and X-axis centre-points separately.
- Improved documentation.
## [1.0.0](https://github.com/saileille/ehm-graphics-tool/releases/tag/1.0.0)
- First release.