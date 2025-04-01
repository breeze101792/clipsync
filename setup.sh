#!/bin/bash
###########################################################
## Vars
###########################################################
export VAR_SCRIPT_NAME="$(basename ${BASH_SOURCE[0]%=.})"
export VAR_CPU_CNT=$(nproc --all)
export VAR_OS='unix'
export VAR_BUILD_TYPE='release'

###########################################################
## Options
###########################################################
export OPTION_VERBOSE=false

###########################################################
## Path
###########################################################
export PATH_ROOT="$(realpath $(dirname ${BASH_SOURCE[0]}))"

###########################################################
## Utils Functions
###########################################################
fPrintHeader()
{
    local msg=${1}
    printf "###########################################################\n"
    printf "###########################################################\n"
    printf "##  %- $((60-4-${#msg}))s  ##\n" "${msg}"
    printf "###########################################################\n"
    printf "###########################################################\n"
    printf ""
}
fErrControl()
{
    local ret_var=$?
    local func_name=${1}
    local line_num=${2}
    if [[ ${ret_var} == 0 ]]
    then
        return ${ret_var}
    else
        echo ${func_name} ${line_num}
        exit ${ret_var}
    fi
}
fHelp()
{
    echo "${VAR_SCRIPT_NAME}"
    echo "[Example]"
    printf "    %s\n" "run test: .sh -a"
    echo "[Options]"
    printf "    %- 16s\t%s\n" "-s|--setup" "setup dependency"
    printf "    %- 16s\t%s\n" "-w|--window" "use windows exe to execute python"
    printf "    %- 16s\t%s\n" "-i|--installer" "generate stand alone windows installer"
    printf "    %- 16s\t%s\n" "-v|--verbose" "Print in verbose mode"
    printf "    %- 16s\t%s\n" "-h|--help" "Print helping"
}
fInfo()
{
    local var_title_pading""

    fPrintHeader ${FUNCNAME[0]}
    printf "###########################################################\n"
    printf "##  Vars\n"
    printf "###########################################################\n"
    printf "##    %s\t: %- 16s\n" "Script" "${VAR_SCRIPT_NAME}"
    printf "###########################################################\n"
    printf "##  Path\n"
    printf "###########################################################\n"
    printf "##    %s\t: %- 16s\n" "Working Path" "${PATH_ROOT}"
    printf "###########################################################\n"
    printf "##  Options\n"
    printf "###########################################################\n"
    printf "##    %s\t: %- 16s\n" "Verbose" "${OPTION_VERBOSE}"
    printf "###########################################################\n"
}
###########################################################
## Functions
###########################################################
function fexample()
{
    fPrintHeader ${FUNCNAME[0]}

}
function fInstaller()
{
    fPrintHeader ${FUNCNAME[0]}
    local var_rel_path='dist'
    local var_version=$(cat core/configtools.py | grep version | cut -d '=' -f 2 | sed "s/'//g")"."$(date +%H%M%S)
    # local var_options=("-m PyInstaller --onefile  --icon=resource/icon.ico")
    local var_options=("-m PyInstaller --onefile ")
    rm -rf ${var_rel_path}
    # if [ "${VAR_BUILD_TYPE}" = 'release' ]
    # then
    #     var_options+=("--noconsole ")
    # fi
    test -d build && rm -rf build
    if [ "${VAR_OS}" = 'win' ]
    then
        python.exe ${var_options[@]} clipsync.py
    else
        python ${var_options[@]} clipsync.py
    fi
    # copy needed files
    # mkdir -p ${var_rel_path}/plugin
    # mkdir -p ${var_rel_path}/scripts
    # cp -rf resource ${var_rel_path}/
    # cp -rf plugin/pluginclient.py ${var_rel_path}/plugin/
    # cp -rf scripts/* ${var_rel_path}/scripts/
    cp ${var_rel_path}/clipsync.exe ${PATH_ROOT}/
    mv ${var_rel_path}/clipsync.exe ${var_rel_path}/clipsync_${var_version}_${VAR_BUILD_TYPE}.exe
    mv ${var_rel_path} clipsync_${var_version}_${VAR_BUILD_TYPE}

    # compress file
    tar cvjf clipsync_${var_version}_${VAR_BUILD_TYPE}.tbz2 clipsync_${var_version}_${VAR_BUILD_TYPE}
    echo "release file: clipsync_${var_version}_${VAR_BUILD_TYPE}.tbz2"
}
function fSetup()
{
    fPrintHeader ${FUNCNAME[0]}
    local var_rel_path='dist'
    local var_pkg_list=("clipboard" "pyinstaller" "cryptography")

    if [ "${VAR_OS}" = 'win' ]
    then
        pip.exe install ${var_pkg_list[@]}
    else
        pip install ${var_pkg_list[@]}
    fi
}
function fSetup_audio()
{
    fPrintHeader ${FUNCNAME[0]}
    local var_rel_path='dist'
    local var_pkg_list=("funasr" "pyaudio" "torch" "torchaudio" "webrtcvad", "opencc")

    if [ "${VAR_OS}" = 'win' ]
    then
        pip.exe install ${var_pkg_list[@]}
    else
        pip install ${var_pkg_list[@]}
    fi
}

## Main Functions
###########################################################
function fMain()
{
    # fPrintHeader "Launch ${VAR_SCRIPT_NAME}"
    local flag_setup=false
    local flag_setup_audio_input=false
    local flag_verbose=false
    local flag_fakeserial=false
    local flag_installer=false

    while [[ $# != 0 ]]
    do
        case $1 in
            # Options
            -s|--setup)
                flag_setup=true
                ;;
            -sa|--setup-audio)
                flag_setup_audio_input=true
                ;;
            -i|--installer)
                flag_installer=true
                if [ "${2}" = "debug" ]
                then
                    VAR_BUILD_TYPE='debug'
                    shift 1
                elif [ "${2}" = "debug" ]
                then
                    VAR_BUILD_TYPE='release'
                    shift 1
                else
                    VAR_BUILD_TYPE='release'
                fi
                ;;
            -w|--window)
                VAR_OS='win'
                ;;
            -v|--verbose)
                flag_verbose=true
                ;;
            -h|--help)
                fHelp
                exit 0
                ;;
            *)
                echo "Unknown Options: ${1}"
                fHelp
                exit 1
                ;;
        esac
        shift 1
    done

    ## Download
    if [ ${flag_verbose} = true ]
    then
        OPTION_VERBOSE=y
        fInfo; fErrControl ${FUNCNAME[0]} ${LINENO}
    fi

    if [ ${flag_setup} = true ]
    then
        fSetup
    fi
    if [ ${flag_setup_audio_input} = true ]
    then
        fSetup_audio
    fi

    if [ ${flag_installer} = true ]
    then
        fInstaller
    fi
}

fMain $@
