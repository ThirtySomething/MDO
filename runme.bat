@echo off
@rem ***************************************************************************
@rem @file runme.bat
@rem ***************************************************************************
@rem @brief Script to handle python environment and startup given script
@rem ***************************************************************************
@rem $Company: MOSCA GMBH, Waldbrunn (Germany), www.mosca.com $
@rem $Copyright: (C) 2021 Mosca GmbH. All rights reserved. $
@rem $Date: 2025-09-02 08:56:29 +0200 (Di, 02 Sep 2025) $
@rem $Revision: 120 $
@rem $Author: Paul $
@rem $HeadURL: http://subvwbn.mosca-ag.com/scm/repo/svn/TestBench/branches/WeldingTestBench/runme.bat $
@rem ***************************************************************************

setlocal EnableDelayedExpansion
@rem ***************************************************************************
@rem * Set base variables, you may tweak here
@rem ***************************************************************************
@rem Set name of python environment
set "ENV_NAME=.venv"
@rem Set name of python environment list exported by pip freeze > %REQ_NAME%
set "REQ_NAME=requirements.txt"
@rem Get name of script to start
set "SCRIPT=%~nx1"
@rem Set default name of script to run
set "DEF_SCRIPT=program"
@rem Set default extension of script to run
set "DEF_SCRIPT_EXT=.py"
@rem Set default suffix of ui script
set "DEF_SCRIPT_UI=UI"
@rem ***************************************************************************
@rem * Set internal variables, don't touch unless you know what you're doing!
@rem ***************************************************************************
@rem Get startup path of script
set "PATH_BASE=%~dp0"
@rem Set FQN of environment
set "PATH_ENVIRONMENT=%PATH_BASE%\%ENV_NAME%"
@rem ***************************************************************************
@rem * Check environment for existence
@rem ***************************************************************************
if not exist "%PATH_ENVIRONMENT%" (
    @rem Create environment
    echo.Create missing environment [%ENV_NAME%]
    python -m venv %ENV_NAME%
    @rem Activate environment
    if ""=="%VIRTUAL_ENV%" (
        echo.Initial activation of environment [%ENV_NAME%]
        call ./%ENV_NAME%/Scripts/activate.bat
    )
    @rem Install required modules
    if exist "%REQ_NAME%" (
        echo.Install required modules in [%REQ_NAME%] to [%ENV_NAME%]
        type %REQ_NAME%
        pip install -r %REQ_NAME%
    ) else (
        echo.List of required modules [%REQ_NAME%] not found
    )
)
@rem ***************************************************************************
@rem * Activate environment if not already done
@rem ***************************************************************************
if ""=="%VIRTUAL_ENV%" (
    echo.Activate environment [%ENV_NAME%]
    call ./%ENV_NAME%/Scripts/activate.bat
)
@rem ***************************************************************************
@rem * Determine script to run, if no name is passed, set default value
@rem ***************************************************************************
if ""=="%SCRIPT%" (
    if exist "%DEF_SCRIPT%%DEF_SCRIPT_UI%%DEF_SCRIPT_EXT%" (
        set "SCRIPT=%DEF_SCRIPT%%DEF_SCRIPT_UI%%DEF_SCRIPT_EXT%"
    ) else (
        set "SCRIPT=%DEF_SCRIPT%%DEF_SCRIPT_EXT%"
    )
)
@rem ***************************************************************************
@rem * Execute script
@rem ***************************************************************************
if exist "%SCRIPT%" (
    echo.Execute script [%SCRIPT%]
    python %SCRIPT%
) else (
    echo.Script [%SCRIPT%] not found, abort
)
endlocal
