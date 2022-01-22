from executions import utils
from executions.models import Execution
from executions.queue import producer
from targets.models import TargetEndpoint
from tasks.models import Task
from tools.executor.callback import tool_callback
from tools.models import Argument, Intensity


def execute(task: Task) -> None:
    '''Execute a task that requests a tool execution.

    Args:
        task (Task): Task that requests a tool execution
    '''
    # Get requested intensity entity
    intensity = Intensity.objects.filter(tool=task.tool, value=task.intensity).first()
    arguments = Argument.objects.filter(tool=task.tool).all()                   # Get arguments for requested tool
    targets = list(task.wordlists.all())                                        # Wordlists are included in targets
    targets.append(task.target)                                                 # Add task target to targets
    targets.extend(list(task.target.target_ports.all()))                        # Add task target ports to targets
    # Add task target endpoints to targets
    targets.extend(list(TargetEndpoint.objects.filter(target_port__target=task.target).all()))
    # Get the executions required for this job based on targets and tool arguments.
    # A job can need multiple executions. For example, if the user includes more than one Wordlist and
    # the tool is Dirsearch that only accepts one wordlist as argument. Rekono will
    # generate one Dirsearch execution for each wordlist provided by the user. It can also occur with
    # TargetPort and TargetEndpoint.
    executions = utils.get_executions_from_findings(targets, task.tool)
    for execution_targets in executions:                                        # For each job execution
        execution = Execution.objects.create(task=task)                         # Create the Execution entity
        # 'update_fields' not specified because this function is called after Execution creation
        execution.save()
        # Enqueue the execution in the executions queue
        producer.producer(
            execution=execution,
            intensity=intensity,
            arguments=arguments,
            targets=execution_targets,
            callback=tool_callback
        )
