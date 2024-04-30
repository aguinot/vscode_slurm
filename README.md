# vscode_candide

Allow one to start `VSCode tunnel` in CANDIDE compute nodes.

## Setup VSCode on CANDIDE

You can find information [here](https://code.visualstudio.com/docs/remote/tunnels).

&emsp;1\. Get VSCode CLI on CANDIDE
   ```bach
    curl -Lk 'https://code.visualstudio.com/sha/download?build=stable&os=cli-alpine-x64' --output vscode_cli.tar.gz
    tar -xf vscode_cli.tar.gz
   ```
Once you have un-tar the archive you will get an executable code which you can add to your PATH.  

&emsp;2\. Setup the tunnel on CANDIDE (this is done only once).
```bach
code tunnel
```

&emsp;3\. Setup the tunnel localy. Follow the instruction [here](https://code.visualstudio.com/docs/remote/tunnels#_using-the-vs-code-ui).

## Install the script

`pip install .`

## Code options

`-h`  
&emsp;Help message.

`mode`  
&emsp;`start`: Open the tunnel  
&emsp;`stop`: Close the tunnel  
`--ssh_command`  
&emsp;Allow one to specify a different ssh command to access CANDIDE.  
&emsp;Default: `ssh candide.iap.fr`  
`--n_cpu`  
&emsp;Specify the number of CPU to use.  
&emsp;Default: 1  
`--mem`  
&emsp;Specify the amount of memory per CPU to use (inGo).  
&emsp;Default: 8  
`--time`  
&emsp;Specify the walltime for the job. The format is the same as the one use in sbatch.  
&emsp;Default: 4:00:00  
`--log`  
&emsp;Specify where to store the log file from sbatch command on CANDIDE.  
&emsp;Note: if you want to use an environment variable such as `$HOME`, it has to done as `\$HOME`.  
&emsp;Default: `\$HOME/vscode_tunnel.log`  
`--node`  
&emsp;Specify on which node to open the tunnel. Use the node names from the cluster.  
&emsp;Note: If you don't specify the right partition you might get an error.  
&emsp;Default: Let the cluster decide.  
`--partition`  
&emsp;Specify which sbatch partion to use.  
&emsp;Default: Let the cluster decide.  
`--exclusive`  
&emsp;Specify if the job should be exclusive.  

### Using the tunnel
* To open a tunnel:
  * `vscode_candide start`
  * `vscode_dandide start --n_cpu=10 --time=10:00:00 --node=n03`
  * `vscode_dandide start --exclusive`
* To close the tunnel:
  * `vscode_candide stop`

Once the tunnel is open, the remote server will be available in VSCode.
