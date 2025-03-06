<h1 align="center">KiCad 8/9 Template for CI/CD with KiBot</h1>

<p align="center">
  <a href=https://www.kicad.org/>
    <img alt="Light" src="https://gitlab.com/uploads/-/system/group/avatar/6593371/kicadlogo.png" height=200>
  </a>
&nbsp; &nbsp; &nbsp; &nbsp;
  <a href=https://kibot.readthedocs.io/en/latest/>
    <img alt="Dark" src="https://raw.githubusercontent.com/INTI-CMNB/KiBot/dev/docs/images/kibot_740x400_logo.png" height=200>
  </a>
</p>

A **KiCad 8/9** template for **automated**, professional documentation generation with **Continuous Integration and Continuous Development** (CI/CD) using [KiBot](https://github.com/INTI-CMNB/KiBot/tree/master). KiCad 9 support is still experimental.

A video tutorial for setting up this template is available [here]().

An example project using this template can be found [here](https://github.com/nguyen-v/amulet_controller_kibot/tree/master).

> [!NOTE]
> This file will be overridden by a KiBot run.

## TABLE OF CONTENTS

- [TABLE OF CONTENTS](#table-of-contents)
- [FEATURES](#features)
- [GETTING STARTED](#getting-started)
- [USAGE](#usage)
  - [CI/CD Workflow and Semantic Versioning](#cicd-workflow-and-semantic-versioning)
  - [Running Locally](#running-locally)
  - [Calculating Board Costs (KiCost)](#calculating-board-costs-kicost)
  - [Visualizing Outputs in a Webpage](#visualizing-outputs-in-a-webpage)
- [PROJECT CONVERSION GUIDE](#project-conversion-guide)
  - [Folders](#folders)
  - [Schematic](#schematic)
  - [PCB](#pcb)
  - [Summary in table format](#summary-in-table-format)
- [DIRECTORY STRUCTURE](#directory-structure)
- [CREDITS](#credits)
- [RESOURCES](#resources)
- [CONTRIBUTING](#contributing)

## FEATURES

- **Automated fabrication document**: [Example](https://github.com/nguyen-v/amulet_controller_kibot/blob/master/Manufacturing/Fabrication/amulet_controller-fabrication.pdf). The stackup table, fabrication notes, drill drawings/tables, testpoint tables/highlighting are all automated.
  
- **Automated assembly document**: [Example](https://github.com/nguyen-v/amulet_controller_kibot/blob/master/Manufacturing/Assembly/amulet_controller-assembly.pdf). The images, tables, DNP crosses, texts are all automated.

- **Automated table of contents** in schematic

- **Automated 3D images** of the PCB in various documents

- **Synchronised `CHANGELOG.md`** with Revision History page of the schematic

- **Automated README.md**: images and other board information

- **Various outputs** such as gerbers, 3D renders, ERC/DRC reports, BoM, Diff visualizer

- **Modern webpage** for visualizing the generated files and documents

- **Robust workflow** with two branches and semantic versioning

- **Releases with changelog** and assets

- **Can be run locally** with Docker

## GETTING STARTED

1. Go to your KiCad templates folder
   
    **Windows**:

    ```
    cd "C:\Program Files\KiCad\8.0\share\kicad\template"
    ```

    **Linux**:
    ```
    cd /usr/share/kicad/template
    sudo chmod 777 ./
    ```

2. Clone the repository

    ```
    git clone git@github.com:nguyen-v/KDT_Hierarchical_KiBot.git
    ```

3. Install the fonts inside of [`kibot_resources/fonts`](kibot_resources/fonts) if not already installed on the system.

4. A custom color theme ([`Altium_Theme.json`](kibot_resources/colors/Altium_Theme.json)) is also provided in [`kibot_resources/colors`](kibot_resources/colors).
You should move this file to your KiCad Themes folder.

    **Windows**:

    `C:\Users\<USER_NAME>\AppData\Roaming\kicad\8.0\colors`

    **Linux**:

    `~/.config/kicad/8.0/colors`

> [!NOTE]
> In the steps above, replace ```8.0``` with ```9.0``` for KiCad 9

5. Create a new project with:

    **File → New Project From Template** and select `KDT_Hierarchical_KiBot`

6. Create a new `dev` branch. This will be the working branch. 
   
   ```
   git checkout -b dev
   ```
   
7. Modify the following fields in [`kibot_main.yaml`](kibot_yaml/kibot_main.yaml#L556) according to your project:
    ```
      # Metadata ===================================================================

      PROJECT_NAME: Project Name
      BOARD_NAME: Board Name

      COMPANY: Company Name
      DESIGNER: Author

      LOGO: 'Logos/dummy_logo.png'
      GIT_URL: 'https://github.com/nguyen-v/KDT_Hierarchical_KiBot'

      # Preflight ==================================================================

      CHECK_ZONE_FILLS: false
      STACKUP_TABLE_NOTE: external layer thicknesses are specified after plating

      # BoM ========================================================================

      MPN_FIELD: 'Manufacturer Part Number'
      MAN_FIELD: 'Manufacturer'

      # Drill table and drill map parameters =======================================

      GROUP_ROUND_SLOTS: true  # whether or not to group round holes and slots
      GROUP_PTH_NPTH: 'no'  # for drill tables (CSV, PCB Print)
      GROUP_PTH_NPTH_DRL: false  # for .drl files

      # Gerber parameters ==========================================================

      PLOT_REFS: true # reference designators

      # Schematic parameters =======================================================

      COLOR_THEME: Altium_Theme
      SHEET_WKS: ${KIPRJMOD}/Templates/KDT_Template_PCB_GIT_A4.kicad_wks
      FAB_SCALING: 1
      ASSEMBLY_SCALING: 1

      # References to exclude from testpoint highlighting ==========================
      
      EXCLUDE_REFS: '[MB*]' # for components on the PCB but not on the schematic

      # 3D Viewer rotations (in steps) =============================================

      3D_VIEWER_ROT_X: 2
      3D_VIEWER_ROT_Y: -1
      3D_VIEWER_ROT_Z: 1
      3D_VIEWER_ZOOM: -1
      KEY_COLOR: '#00FF00' # background color to remove
    ```

8. The files inside of [`kibot_resources/templates`](kibot_resources/templates) should also be modified according to your project. These include Assembly and Fabrication notes, Impedance table and README file templates.

9. Edit the [`*.kicad_dru`](KDT_Hierarchical_KiBot.kicad_dru) if necessary according to your design rules. Right now, it has been set for PCBWay 6-layer PCBs with 2oz outer 1oz inner, focusing on lowest cost.

10.  Edit the [`kibot_out_csv_bom.yaml`](kibot_yaml/kibot_out_csv_bom.yaml), [`kibot_out_html_bom.yaml`](kibot_yaml/kibot_out_html_bom.yaml) and [`kibot_out_xlsx_bom.yaml`](kibot_yaml/kibot_out_xlsx_bom.yaml) files according to the component fields that you use. You can refer to the [KiCost Documentation](https://hildogjr.github.io/KiCost/docs/_build/singlehtml/index.html) for the field names.

## USAGE

### CI/CD Workflow and Semantic Versioning

This template is meant to be used in a CI/CD environment on GitHub. The workflow is as follows:

- Any custom font used in the project must be added to the [`kibot_resources/fonts`](kibot_resources/fonts) folder.

> [!NOTE]
> KiCad 9 allows for fonts to be embedded in the schematic. However, it is still good practice to add the fonts in the folder mentioned.

- There are two branches, a `main` and a `dev` branch. The `dev` branch is the working branch. The `main` should only be used for pull requests and releases.

- Changes should be recorded in the [`CHANGELOG.md`](CHANGELOG.md) file, and should respect [semantic versioning guidelines](https://semver.org/) for [hardware](https://www.maskset.net/blog/2023/02/26/semantic-versioning-for-hardware/). The changes of the current version should be added under the `[Unreleased]` section.

- The `variant` variable in [.github/workflows/ci.yaml](.github/workflows/ci.yaml#L21) should be selected according to the project progress.

  ```
    # Used variant. We assume:
    # DRAFT: only schematic in progress, will only generate schematic PDF, netlist and BoM
    # PRELIMINARY: will generate both schematic and PCB documents, but no ERC/DRC
    # CHECKED: will generate both schematic and PCB documents, with ERC/DRC
    # RELEASED: similar to CHECKED, automatically selected when pushing a tag to master

    kibot_variant: CHECKED  
  ```

- The `kicad_version` variable in [.github/workflows/ci.yaml](.github/workflows/ci.yaml#L24) should be selected according to the desired KiCad version. Supported versions are 8 and 9.

- You should work locally on the `dev` branch. When a change is made, the changes should be pushed to GitHub which will trigger the KiBot workflow. The generated files will be committed and pushed back to the repository.

- After a successful KiBot run on the remote repository, you should pull back the changes into your local repository.

- To avoid conflicts, you should avoid modifying the `.kicad_pro` file locally before pulling from the remote (after the completion of a KiBot run). Otherwise, you will need to solve merge conflicts when pulling the file.

- To synchronise the Revision History of the schematic with the `CHANGELOG.md` file, you should create new text variables in [kibot_pre_set_text_variables.yaml](kibot_yaml/kibot_pre_set_text_variables.yaml#L39). The text variables should then be added in the text boxes of the Revision History sheet.

  ```
  - variable: '@RELEASE_TITLE_VAR@x.x.x'
    command: '@GET_TITLE_CMD@ x.x.x'
  - variable: '@RELEASE_BODY_VAR@x.x.x'
    command: '@GET_BODY_CMD@ x.x.x'
  ```

- When ready for a release, you should open a pull request and merge the changes into main. Currently the workflow is set **not to trigger on pull requests**, as we assume the changes coming from `dev` are up-to-date.

- To create a release, push a tag on the `main` branch with the version number (for example `x.x.x = 1.1.1`):

  ```
  git checkout main
  git pull
  git tag x.x.x
  git push origin x.x.x
  ```

  This will start a KiBot run with the variant set as `RELEASED`. When the run completes, it also creates a release with assets and updates the `CHANGELOG.md` file (renames the `[Unreleased]` section with the pushed tag and creates a new `[Unreleased]` section).

- After a release, you will need to update your `main` branch to be up-to-date with the remote:

  ```
  git pull
  ```

  And you will also need to rebase your `dev` branch to the `main` branch:

  ```
  git checkout dev
  git rebase main
  ```

> [!NOTE]
> You are free to modify the [.github/workflows/ci.yaml](.github/workflows/ci.yaml) file to suit your workflow needs.

***

### Running Locally

KiBot can be installed if you want to run some of the scripts locally. If you only plan to use it in a CI/CD workflow, this step can be skipped.
Installation steps can be found on the [official documentation](https://kibot.readthedocs.io/en/master/installation.html). 
The easiest way to install KiBot if custom development is not required is with dockers.

1.  Install **and run** [Docker Desktop](https://docs.docker.com/desktop/)
  
2.  Run the script `docker_kibot_windows.bat` or `docker_kibot_linux.sh` depending on your platform in [`kibot_resources/scripts`](kibot_resources/scripts). Currently tested on Windows and WSL2. This should pull and start a docker running the `dev` branch of KiBot. You should have access to your local files.

***
**KiCad 8**

  Windows:

  ```
  .\docker_kibot_windows.bat
  ```

  Linux:

  ```
  ./docker_kibot_linux.sh
  ```

***
**KiCad 9**

  Windows:

  ```
  .\docker_kibot_windows.bat -v 9
  ```

  Linux:

  ```
  ./docker_kibot_linux.sh -v 9
  ```
  ***

Once in the docker, you can use the [`kibot_launch.sh`](kibot_launch.sh) script to generate and visualize outputs.

```
./kibot_launch.sh
```

You can get more information about the usage with

```
./kibot_launch.sh --help
```

When running the script with no arguments, it will default to the `CHECKED` variant and generate all outputs. A variant can be set with the `-v` flag. If a custom variant is used (i.e. other than the default variants `DRAFT`, `PRELIMINARY`, `CHECKED`, `RELEASED`), the outputs will be generated in the `Variants` folder.

Each default variant will have different KiBot flags, which is useful for different phases of the project:


1. **DRAFT**
  
   Only schematic in progress, will only generate schematic PDF, netlist and BoM

2. **PRELIMINARY**
   
   Will generate both schematic and PCB documents, but no ERC/DRC

3. **CHECKED**
   
   Will generate both schematic and PCB documents, with ERC/DRC

4. **RELEASED**
   
   Similar to CHECKED, automatically selected when pushing a tag to main (CI/CD)

> [!WARNING]
> When generating outputs locally, it could conflict with the outputs generated by the remote CI/CD workflow. In this case, you should decide how to resolve the conflicts.

***

### Calculating Board Costs (KiCost)

[KiCost](https://github.com/hildogjr/KiCost) is used to estimate costs and get a nice XLSX spreadsheet with part specs. In this project, we run KiCost locally to avoid too many API calls. Also, DigiKey's API [doesn't seem to work](https://github.com/set-soft/kicost_ci_test) in a CI/CD environment.
To run KiCost, you will need to create a file `kicost_config_local.yaml` in [`kicost_yaml`](kicost_yaml). You can use the [`kicost_config_local_template.yaml`](kicost_yaml/kicost_config_local.yaml) file as a base. Once you have filled in the API keys for the desired manufacturers, KiCost can be run with:

```
./kibot_launch.sh --costs
```
This will create a spreadsheet in [`Manufacturing/Assembly`](Manufacturing/Assembly/) folder.

You can also specify a variant if desired:

```
./kibot_launch.sh -v <VARIANT> --costs
```

For more information, please have a look at the official [documentation](https://hildogjr.github.io/KiCost/docs/_build/singlehtml/index.html)

> [!CAUTION]
> KiCost expects the **MPN (Manufacturer Part Number)** and **Manufacturer** fields to be named in a certain way. To cater for different naming conventions, we rename user-defined fields to KiCost-compatible fields in the KiBot run. You can set your user-defined field for **MPN** and **Manufacturer** in the [`kibot_yaml/kibot_main.yaml`](kibot_yaml/kibot_main.yaml#L576) by editing the `MPN_FIELD` and `MAN_FIELD` definitions.

<p align="center">
  <img alt="XLSX BoM" src="https://github.com/user-attachments/assets/e7683ae3-efcc-4f64-b4b7-c4c39c3c9d48">
</p>

<p align="center">
  <img alt="XLSX Costs" src="https://github.com/user-attachments/assets/1136a095-fc2d-4f59-bcbf-24f6e1a69410">
</p>

<p align="center">
  <img alt="XLSX Specs" src="https://github.com/user-attachments/assets/77677761-7ab1-4580-b60c-6a0563c59d67">
</p>

***

### Visualizing Outputs in a Webpage

The outputs of KiBot can be visualized in a webpage (excepted for the `DRAFT` variant). This can be done by running:

```
./kibot_launch.sh --server
```
And opening `http://localhost:8000` in your favorite browser. The server can be shut down with:
```
./kibot_launch.sh --stop-server
```

> [!TIP]
> You can also give the port as an argument if you want to use another port.

<p align="center">
  <img alt="Web Page" src="https://github.com/user-attachments/assets/9abee686-5245-4850-b00f-b67be02284ee">
</p>

## PROJECT CONVERSION GUIDE

This section will describe the necessary steps to convert an existing project to work with this template. This will also give more insights into how the template works in general. For more information, you should refer to the template.

***

### Folders

You should keep the folder structure as defined in [DIRECTORY STRUCTURE](#directory-structure). The folders marked as optional are not mandatory for the project to work, as long as the relevant file paths are correct (e.g. logos). You should then go through the same steps as in [GETTING STARTED](#getting-started) and [USAGE](#usage).

### Schematic

You should select [`Templates/KDT_Template_GIT.kicad_wks`](Templates/KDT_Template_GIT.kicad_wks) as your Drawing Sheet in:

**File → Page Settings → Drawing Sheet**

On the same page, The `Revision` and `Company` fields should be set to `${REVISION}` and `${COMPANY}` and exported to all sheets.

<p align="center">
  <img alt="Drawing Sheet" src="https://github.com/user-attachments/assets/311f4e13-cdb9-45cb-9fcf-1a88f8432416">
</p>

For an automated table of contents, you should copy the root page of the template into your project, or use the `${SHEET_NAME_X}` text variables. These variables will be replaced by the sheet name (page `X`) when running KiBot. Currently the maximum number of pages is set to 40. You are free to add new text variables in [`kibot_yaml/kibot_pre_set_text_variables`](kibot_yaml/kibot_pre_set_text_variables.yaml#L160).

The `${VARIANT}` text variable is replaced by the current variant name (e.g. DRAFT or RELEASED). 

The `${RELEASE_DATE}` and `${RELEASE_DATE_NUM}` will be replaced by the tag release date and are just the same date in different formats (for example, `${RELEASE_DATE} = 17-Dec-2024` and `${RELEASE_DATE_NUM} = 2024-12-17`).

To get 3D pictures of the PCB in the schematic, you can create text boxes with the desired size, with the following names: `kibot_image_png_3d_viewer_angled_top` and `kibot_image_png_3d_viewer_angled_bottom`.

<p align="center">
  <img alt="kibot_image_png_3d_viewer_angled_top, kibot_image_png_3d_viewer_angled_bottom" src="https://github.com/user-attachments/assets/2f7f23fa-e233-4a54-b656-860f69a33d36">
</p>

> You can add any image generated by a KiBot output using by changing the name to `kibot_image_<output_name>`.



To synchronise the Revision History of the schematic with the `CHANGELOG.md` file, you should create new text variables in [kibot_pre_set_text_variables.yaml](kibot_yaml/kibot_pre_set_text_variables.yaml#L39). The text variables (`${RELEASE_TITLE_VAR<VERSION>}` and `${RELEASE_BODY_VAR<VERSION>`) should then be added in the text boxes of the Revision History sheet.

  ```
  - variable: '@RELEASE_TITLE_VAR@x.x.x'
    command: '@GET_TITLE_CMD@ x.x.x'
  - variable: '@RELEASE_BODY_VAR@x.x.x'
    command: '@GET_BODY_CMD@ x.x.x'
  ```

***

### PCB

The layer names of the PCB should follow the ones defined in [kibot_main.yaml](kibot_yaml/kibot_main.yaml#L631). 

```
  LAYER_TITLE_PAGE: TitlePage
  LAYER_DNP_TOP: F.DNP
  LAYER_DNP_BOTTOM: B.DNP
  LAYER_DRILL_MAP: DrillMap
  LAYER_TP_LIST_TOP: F.TestPointList
  LAYER_TP_LIST_BOTTOM: B.TestPointList
  LAYER_ASSEMBLY_TEXT_TOP: F.AssemblyText
  LAYER_ASSEMBLY_TEXT_BOTTOM: B.AssemblyText
  LAYER_DNP_CROSS_TOP: F.DNP
  LAYER_DNP_CROSS_BOTTOM: B.DNP
```

<p align="center">
  <img alt="PCB Layer Names" src="https://github.com/user-attachments/assets/9089a324-e170-4cd5-ae4f-396ef3fdd1c9">
</p>

The layer names can be set in 

**File → Board Setup → Board Stackup → Board Editor Layers**

Each layer has a specific function, and must be setup in a particular way.

In the following explanation, when a group must be created, this can be done using KiCad's **Draw Rectangle** tool, and then a group can be created with:

**Right-Click → Grouping → Group Items**

Pressing **E** then allows you to rename the group. The size and position of the group usually determines the size and location of the element to be drawn. To change the font inside a group, you can create a textbox with the desired font in the group. You can set the border width to 0.

<p align="center">
  <img alt="Textbox Group" src="https://github.com/user-attachments/assets/b7956436-d8df-47e1-a082-ca6bbaeae168">
</p>

***

**TitlePage**

This is used for the first page of the assembly document. Here, you should add **Top View** and **Bottom View** texts and under these text, you can create two named groups with the location and size that you desire. The groups should be named `kibot_image_png_3d_viewer_angled_top` and `kibot_image_png_3d_viewer_angled_bottom`.

> [!TIP]
> You can add any image generated by a KiBot output using by changing the name to `kibot_image_<output_name>`.

<p align="center">
  <img alt="TitlePage" src="https://github.com/user-attachments/assets/38470acb-2645-42eb-b38f-222b4a6475b2">
</p>

<p align="center">
  <img alt="kibot_image_png_3d_viewer_angled_top" src="https://github.com/user-attachments/assets/8b8d1beb-7f2a-4339-a4be-258da6ff926a" width="45%">
&nbsp; &nbsp; &nbsp; &nbsp;
  <img alt="kibot_image_png_3d_viewer_angled_bottom" src="https://github.com/user-attachments/assets/1419a4bd-6247-4eb8-a410-cb4665220ba2" width="45%">
</p>

***

**User.Comments**

Currently not used, you can use it for your project.

***

**F.DNP** and **B.DNP**

These are used to hold the red crosses for components marked as *Do Not Populate*. The layers for those should be kept empty.

***

**DrillMap**

This layer is used to draw drill map drawings and drill tables in the fabrication document. You should create a named group called `kibot_table_csv_drill_table` and place it where the drill tables should be drawn for each drill layer pair. The drill drawing is by default aligned with the PCB.

<p align="center">
  <img alt="DrillMap" src="https://github.com/user-attachments/assets/018821a7-890a-45a8-b4b7-07eb7e3e8bcf">
  <img alt="kibot_table_csv_drill_table" src="https://github.com/user-attachments/assets/e35f71d1-dbdf-42ec-8f02-b95118e12bdb">
</p>

***

**F.TestPoint** and **B.TestPoint**

These layers are used to highlight testpoint locations in the fabrication document. They should be left as empty.

***

**F.AssemblyText**

This layer is used to hold information about the number of components, assembly notes, assembly drawing and 3D render of the top of the PCB. For the number of components, you should create a group named `kibot_table_csv_comp_count`. Assembly notes should be added using the text variable `${ASSEMBLY_NOTES}`. The 3D render can be added by creating a group named `kibot_image_png_3d_viewer_top`.

<p align="center">
  <img alt="F.AssemblyText" src="https://github.com/user-attachments/assets/3ecbb012-ad26-4e94-9fb2-f2743e7ff44e">
  <img alt="kibot_image_png_3d_viewer_top" src="https://github.com/user-attachments/assets/823c4d2a-d84a-4096-b277-c7938554fb98">
</p>

<p align="center">
  <img alt="kibot_table_csv_comp_count" src="https://github.com/user-attachments/assets/e05bb55f-971e-4b34-9af6-0b44668ae599" width="45%">
&nbsp; &nbsp; &nbsp; &nbsp;
  <img alt="${ASSEMBLY_NOTES}" src="https://github.com/user-attachments/assets/954b444f-8db9-4e08-85c1-5c62ee96d5fa" width="45%">
</p>

**B.AssemblyText**

This layer hold the assembly drawing and 3D render for the backside of the PCB. For the 3D render, you should add a group named `kibot_image_png_3d_viewer_bottom`.

***

**F.Dimensions**

This layer holds information about the PCB stackup and dimensions, impedance table and fabrication notes. The PCB stackup can be added by creating a group named `kibot_fancy_stackup`. The impedance table with a group named `kibot_table_csv_impedance_table` and the fabrication notes are included with the text variable `${FABRICATION_NOTES}`.

> [!NOTE]
> The text variable ${FABRICATION_NOTE} is dependent on the [`kibot_resources/templates/fabrication_notes.txt`](kibot_resources/templates/fabrication_notes.txt) file. Modify it to your needs.

<p align="center">
  <img alt="F.Dimensions" src="https://github.com/user-attachments/assets/6f47fa22-8bc8-4a65-97d7-891e124f82a2">
  <img alt="kibot_fancy_stackup" src="https://github.com/user-attachments/assets/bb45fed2-820a-48a4-b8c7-9473efa5007a">
</p>

<p align="center">
  <img alt="kibot_table_csv_impedance_table" src="https://github.com/user-attachments/assets/add357a8-4aee-4d9d-873f-08883d448c07">
  <img alt="${FABRICATION_NOTES}" src="https://github.com/user-attachments/assets/82083591-50fe-4381-b643-ba91a7d45452">
</p>

**B.Dimensions**

This layer contains information about the dimensions of the PCB, seen from the backside. Similarly to the front side, you can use KiCad's **Dimensions** tool to add some dimensions.

<p align="center">
  <img alt="B.Dimensions" src="https://github.com/user-attachments/assets/cd62501d-b696-49f7-a9a5-9cf350b76d70">
</p>

***

**F.TestPointList**

This layer is used to hold information about the testpoints locations and nets. You can add testpoint tables by creating a group named `kibot_table_csv_testpoints_top`. It is also possible to use python slicing to separate the table into multiple tables, by using slice operators in the name. For example: `kibot_table_csv_testpoints_top[:32]` and `kibot_table_csv_testpoints_top[32:]` in two different groups would create two tables with the first one including the first 32 testpoints and the second one every testpoint after that.

Test point locations are computed from the drill origin, which can be set with:

**Place → Drill/Place File Origin**.

> [!TIP]
> It is usually good practice to set the origin at the bottom left of the board.

<p align="center">
  <img alt="F.TestPointList" src="https://github.com/user-attachments/assets/ec1e538e-05f0-4e3b-a5b7-642a60116f10">
</p>

<p align="center">
  <img alt="kibot_table_csv_testpoints_top[:32]" src="https://github.com/user-attachments/assets/4c69e9e0-461f-4de7-9528-34ebe5d93b9c" width="45%">
&nbsp; &nbsp; &nbsp; &nbsp;
  <img alt="kibot_table_csv_testpoints_top[32:]" src="https://github.com/user-attachments/assets/d77a5d2c-f599-49e7-801b-01bb4950e769" width="45%">
</p>

**B.TestPointList**

Similar to the front testpoint layer. The group should be named `kibot_table_csv_testpoints_bottom`. Note that because PCB is inverted for this layer during print, if the group is placed on the left side it will be printed on the right side.

<p align="center">
  <img alt="B.TestPointList" src="https://github.com/user-attachments/assets/e1f6cd3a-5322-4699-9ae8-d9e4d9d16b93">
</p>

<p align="center">
  <img alt="kibot_table_csv_testpoints_bottom" src="https://github.com/user-attachments/assets/42e035fa-a4c3-4251-81da-6ff4a5da102e">
</p>

***

### Summary in table format

| **Layer**                     | **Description**                                                                                    | **Changes/Included Items**                                                                                                    |
|-------------------------------|----------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------|
| **TitlePage**                 | First page of the assembly document.                                                               | Add groups: `kibot_image_png_3d_viewer_angled_top` and `kibot_image_png_3d_viewer_angled_bottom`.                             |
| **User.Comments**             | Reserved for project-specific comments.                                                            | Not used by default; customize as needed.                                                                                     |
| **F.DNP / B.DNP**             | Holds red crosses for components marked as *Do Not Populate*.                                      | Keep these layers empty.                                                                                                      |
| **DrillMap**                  | Draws drill map drawings and tables in the fabrication document, aligned by default with the PCB.  | Add group: `kibot_table_csv_drill_table`.                                                                                     |
| **F.TestPoint / B.TestPoint** | Highlights testpoint locations in the fabrication document.                                        | Keep these layers empty.                                                                                                      |
| **F.AssemblyText**            | Contains component count, assembly notes, drawings, and 3D renders for the top side of the PCB.    | Add group: `kibot_table_csv_comp_count` (table) and `kibot_image_png_3d_viewer_top` (image). Include `${ASSEMBLY_NOTES}` text.|
| **B.AssemblyText**            | Holds assembly drawings and 3D render for the bottom side of the PCB.                              | Add group: `kibot_image_png_3d_viewer_bottom` for the 3D render.                                                              |
| **F.Dimensions**              | Holds PCB stackup, dimensions, impedance table, and fabrication notes.                             | Add groups: `kibot_fancy_stackup` (stackup), `kibot_table_csv_impedance_table` (impedance table), and `${FABRICATION_NOTES}`. |
| **B.Dimensions**              | Holds dimensions of the PCB, seen from the backside.                                               | Use KiCad **Dimensions** tool to add details.                                                                                 |
| **F.TestPointList**           | Lists testpoint locations and nets for the top layer.                                              | Add group: `kibot_table_csv_testpoints_top`. Use slicing (e.g., `[:32]`) for multiple tables.                                 |
| **B.TestPointList**           | Lists testpoint locations and nets for the bottom layer.                                           | Add group: `kibot_table_csv_testpoints_bottom`. Adjust left-side placements for inverted print alignment.                     |

## DIRECTORY STRUCTURE
The following directory structure is used in the template. Folders marked as 'optional' are not crucial for KiBot to work. Other folders will be generated automatically during a KiBot run.

```
├─ Computations       # Misc calculations (optional)
├─ HTML               # HTML files for generated webpage
├─ Images             # Pictures and renders
│
├─ kibot_resources
│  ├─ colors          # Color theme for KiCad
│  ├─ fonts           # Fonts used in the project
│  ├─ scripts         # External scripts used with KiBot
│  └─ templates       # Templates for KiBot generated reports
│
├─ kibot_yaml         # KiBot YAML config files
├─ KiRI               # KiRI (PCB diff viewer) files
│
├─ lib                # Footprint and symbol libraries (optional)
│  ├─ 3d_models       # Component 3D models
│  ├─ lib_fp          # Footprint libraries
│  └─ lib_sym         # Symbol libraries
│
├─ Logos              # Logos (optional)
│
├─ Manufacturing
│  ├─ Assembly        # Assembly documents (BoM, pos, notes)
│  │
│  └─ Fabrication     # Fabrication documents (ZIP, notes)
│     ├─ Drill Tables # CSV drill tables
│     └─ Gerbers      # Gerbers
│
├─ Report             # Reports for ERC/DRC
├─ Schematic          # PDF of schematic
├─ Templates          # Title block templates
├─ Testing
│  └─ Testpoints      # Testpoints tables      
│
└─ Variants           # Outputs for assembly variants (optional)
```

## CREDITS

[@set-soft](https://github.com/set-soft) for his amazing work on [KiBot](https://github.com/INTI-CMNB/KiBot/tree/master). Check out the [documentation](https://kibot.readthedocs.io/en/latest/) for more!

## RESOURCES

- [Video Tutorial for this template]()

- [Example project (from the video tutorial)](https://github.com/nguyen-v/KiBot_Project_Test)

- [Example project (Amulet)](https://github.com/nguyen-v/amulet_controller_kibot/tree/master)

- [(Outdated) Best practices and tips for good schematics](https://www.youtube.com/watch?v=_ZjyeltLMAg)

- [GitHub Actions Documentation](https://docs.github.com/en/actions)

- [KiBot Documentation](https://kibot.readthedocs.io/en/latest/)

- [KiBot Repository](https://github.com/INTI-CMNB/KiBot)

- [KiCost Documentation](https://hildogjr.github.io/KiCost/docs/_build/singlehtml/index.html)

- [KiCost Repository](https://github.com/hildogjr/KiCost)

- [KiRI Repository](https://github.com/leoheck/kiri)

## CONTRIBUTING

Feel free to open a pull request if you have any cool features to add!
