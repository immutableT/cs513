## Setting Up Code and Installing Requirements

1. Ensure python https://www.python.org/downloads/  
          git https://git-scm.com/book/en/v2/Getting-Started-Installing-Git  
          pip https://pip.pypa.io/en/stable/installation  
          java http://docs.oracle.com/javase/7/docs/webnotes/install/ (optional for YesWorkflow setup, see below)    
   are all up to date

2. Clone the repository from github with the following command

    ``` 
    git clone https://github.com/immutableT/cs513.git 
    ```

3. Navigate to the repository with your console. It is recommended to setup a virtual environment for installing python packages. Install requirements using the following command

    ``` 
    pip install -r requirements.txt 
    ```
    
4. (Optional) Set up YesWorkflow. If running YesWorkflow is desired to generate provenance diagrams, Java must be at version 1.7 or higher. Set up YesWorkflow following this guide https://github.com/yesworkflow-org/yw-prototypes but an abridged version is provided below.  
    a. Install Graphviz http://graphviz.org/Download.php ensuring ```dot``` command is in your path.  
    b. Download YesWorkflow Jar https://github.com/yesworkflow-org/yw-prototypes/releases/download/v0.2.0/yesworkflow-0.2.0-jar-with-dependencies.jar  
    c. Define short command on command line.  
    For Linux:  
    ```
    alias yw='java -jar %REPLACE DIRECTORY%/yesworkflow-0.2.0-jar-with-dependencies.jar' 
    ```
        
    For Windows:  
        
    ```
    doskey yw=java -jar %REPLACE DIRECTORY%\yesworkflow-0.2.0-jar-with-dependencies.jar $*
    ```  

## Running Code

Navigate to directory where main.py is located and run 

``` 
python main.py 
```

## Generating Provenance Using YesWorkflow

If YesWorkflow was installed earlier, it will be possible to recreate the diagram located at workflow.png. If setup correctly this process is very simple, as yw.properties will take care of most of the work. Run these 2 commands from the directory:

```
yw graph  
dot -Tpng combined.gv -o workflow.png 
```
        
