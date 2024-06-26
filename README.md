# vscode_slurm

Allow one to start `VSCode tunnel` on Slurm compute nodes.

## Setup VSCode on the cluster

You can find information [here](https://code.visualstudio.com/docs/remote/tunnels).

&emsp;1\. Get VSCode CLI on the cluster
   ```bach
    curl -Lk 'https://code.visualstudio.com/sha/download?build=stable&os=cli-alpine-x64' --output vscode_cli.tar.gz
    tar -xf vscode_cli.tar.gz
   ```
Once you have un-tar the archive you will get an executable code which you can add to your PATH.  

&emsp;2\. Setup the tunnel on the cluster (this is done only once).
```bach
code tunnel
```
**Note**: It is possible that you need re-authenticate later. If the connection does not start, check the log file (`--log` below), it will contain a link and a code to authenticate. It looks like authentication through token is under development (see [here](https://learn.microsoft.com/en-us/azure/developer/dev-tunnels/cli-commands)).

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
&emsp;Allow one to specify a different ssh command to access a cluster.  
&emsp;Default: `ssh candide.iap.fr`  
`--slurm_dir`  
&emsp;Allow one to specify a different slurm directory.  
&emsp;Default: `/usr/local/slurm/latest/bin/`  
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
&emsp;Specify where to store the log file from sbatch command on the cluster.  
&emsp;Default: `\$HOME/vscode_tunnel.log`  
&emsp;**Note**: if you want to use an environment variable such as `$HOME`, it has to done as `\$HOME`.  
`--node`  
&emsp;Specify on which node to open the tunnel. Use the node names from the cluster.  
&emsp;Default: Let the cluster decide.  
&emsp;**Note**: If you don't specify the right partition you might get an error.  
`--partition`  
&emsp;Specify which sbatch partion to use.  
&emsp;Default: Let the cluster decide.  
`--exclusive`  
&emsp;Specify if the job should be exclusive.  

### Using the tunnel
* To open a tunnel:
  * `vscode_slurm start`
  * `vscode_slurm start --n_cpu=10 --time=10:00:00 --node=n03`
  * `vscode_slurm start --exclusive`
* To close the tunnel:
  * `vscode_slurm stop`

Once the tunnel is open, the remote server will be available in VSCode.
