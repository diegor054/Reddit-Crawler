@echo off

REM Check if the required arguments are provided
if [%1] == [] goto usage
if [%2] == [] goto usage

REM Set the subreddit and limit variables from the first two arguments
set subreddit=%1
set limit=%2

REM Set the output file name to the third argument or use "data.json" if none
if [%3] == [] (
    set outfile=data.json
) else (
    set outfile=%3
)

REM Call the Python script with the provided arguments
python3.9.exe crawler.py %subreddit% %limit% %outfile%
goto end

:usage
echo Usage: %0 subreddit limit [outfile]
goto end

:end