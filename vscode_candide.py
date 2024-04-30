from argparse import ArgumentParser

import subprocess


JOB_NAME = "VScode_tunnel"
SLURM_DIR = "/usr/local/slurm/latest/bin/"


def get_parser():

    parser = ArgumentParser()
    parser.add_argument(
        "mode",
        help='modes: use "start" to open the tunnel and "stop" to close the '
        'tunnel',
        type=str,
    )
    parser.add_argument(
        "--ssh_command",
        dest="ssh_command",
        default="ssh candide.iap.fr",
        type=str,
        help="command used to ssh the cluster",
    )
    parser.add_argument(
        "--n_cpu",
        dest="n_cpu",
        default=1,
        type=int,
        help="how many cores to use. Default 1",
    )
    parser.add_argument(
        "--mem",
        dest="mem",
        default=8,
        type=int,
        help="how much memory to allocate per cores (in Go). Default 8",
    )
    parser.add_argument(
        "--time",
        dest="time",
        default="4:00:00",
        type=str,
        help="walltime for the job. Default 4h",
    )
    parser.add_argument(
        "--log",
        dest="log",
        default=r"\$HOME/vscode_tunnel.log",
        type=str,
        help='where to save the log (on the cluster). Default '
        '"$HOME/vscode_tunnel.log"',
    )
    parser.add_argument(
        "--node",
        dest="node",
        default=None,
        type=str,
        help="on which node we run VScode. Default let the cluster decide",
    )
    parser.add_argument(
        "--partition",
        dest="partition",
        default=None,
        type=str,
        help="which partition to use to submit the job. Default let the "
        "cluster decide",
    )
    parser.add_argument(
        "--exclusive",
        dest="exclusive",
        action="store_true",
        help="specify if the job should be exclusive"
    )

    return parser


def check_running(args):

    res = subprocess.getoutput(
        f"{args.ssh_command} "
        f"{SLURM_DIR}squeue --me --name={JOB_NAME} --states=R -h -O JobID"
    )
    res = res.strip()

    if res != "":
        try:
            _ = int(res)
            return res
        except ValueError:
            raise Exception(
                f"Something went wrong while requesting JobID: {res}"
            )
    else:
        return res


def main():

    parser = get_parser()

    args = parser.parse_args()

    jobid = check_running(args)
    if args.mode == "stop":
        if jobid == "":
            raise Exception("No tunnel open")
        cmd = f'{args.ssh_command} "{SLURM_DIR}/scancel ' \
            rf' \$({SLURM_DIR}squeue --me --name={JOB_NAME} ' \
            f'--states=R -h -O JobID)"'
    elif args.mode == "start":
        if jobid != "":
            raise Exception(f"Tunnel already open. JobID: {jobid}")
        cmd = f'{args.ssh_command} "{SLURM_DIR}/sbatch --output={args.log} ' \
            f'--job-name={JOB_NAME} --time={args.time} ' \
            f'--cpus-per-task={args.n_cpu} --mem-per-cpu={args.mem}G'
        if args.exclusive:
            cmd += " --exclusive"
        if args.node is not None:
            cmd += f' --nodelist={args.node}'
        if args.partition is not None:
            cmd += f' --partition {args.partition}'
        cmd += r' --wrap \"code tunnel\""'
    else:
        raise ValueError(f'mde must be in ["start", "stop"] got: {args.mode}')

    result = subprocess.getoutput(cmd)

    new_jobid = check_running(args)
    if args.mode == "stop":
        if new_jobid == "":
            print(f"tunnel with JobID: {jobid} closed")
        else:
            raise Exception(
                f"Something went wrong while closing: {new_jobid}"
            )
    if args.mode == "start":
        if new_jobid == "":
            raise Exception(f"Tunnel failed to open: {result.strip()}")
        else:
            print(f"Tunnel with JobID: {new_jobid} open")
