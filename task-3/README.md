# Task 3 - Questions

## Q1

![architecture](./architecture.svg)

In this architecture, three groups of actors were indicated:
* User - the end user of the system, uses the application, in this case the generation of text from the LLM model.
* Dev - ML dev, creating new versions of models or applications and starting the workflow.
* Admin - managing and developing the infrastructure, in particular the ML pipeline, service and cluster configuration.

The end user uses the application, created by teams of devs and admins. A broader description of making the application available to them is included in Q4.

In the case of admins, they are responsible for maintaining pipelines, their development and providing new features related to these issues. They introduce changes to the infra-repo.

Devs create the application and use the pipelines to generate subsequent iterations of the model, mainly to improve their quality. They do not have to interfere with the infra-repo.

The proposed architecture allows for full automation of the implementation of changes sent to the code repository. In the case of app-repo, a CI tool like jenkins or GH Actions can run a pipeline that will push changes to the infra-repo repository, e.g. updating the name or tag of an image. Considering the operation of ArgoCD, it will also trigger a pipeline that will deploy the appropriate changes to ArgoCD Applications, especially in workflow templates. Thanks to this, the dev group has access to the latest features related to the execution of pipelines almost immediately. CI for app-repo can also trigger Argo Workflow.

In addition, the use of Argo Workflows allows for the automation of the process of training, evaluating and deploying models, so that the dev can focus mainly on the implementation of the model code or its use, instead of on the system complexity of the pipeline.

## Q2
While choosing tools, I was guided by two main factors:
* Automation - performing activities in a machine way significantly reduces the risk of making an error that can be either tragic in its consequences or very difficult to detect, and therefore to patch.
* Extensibility - how much the tool, codes or manifests can be extended.
* Support fot templating - the ability to create generic, reusable configs.

Automation and extensibility complement each other - the possibility of extending functionality may increase automation, and automation may be an extension of the possibilities available to different groups of software developers.

Templating speeds up application development. It also reduces the amount of final code, which has a positive impact on the CI/CD pipeline execution times. However, it may lead to increased software complexity and reduced readability, if templates would be _too generic_ (typical case in React HOCs). Both, Argo Workflows and helm charts, that were selected in this project, are natively using templating engines. It allowed to both, preconfigure and customize all of the applications used in the cluster.

This approach allows to skip entirely the requirement to understand Kubernetes and its orchestration mechanisms. Even CI aspects can be a mystery to dev team, but it is not recommended.

## Q3
In _favorable conditions_, devs may not manually trigger the pipeline, but only observe its execution and effects. However, assuming that manual testing is necessary, devs must understand the yaml format, in which variables for workflows are defined, and understand the principle of Argo workflows, including the templates used to create them. In this way, they will be able to consciously trigger the pipelines.

If developing new model functionalities requires changing the pipeline, they must properly communicate the need to the admin team, so that they can prepare an appropriate template.

## Q4
End users can interact with the application via endpoint, provided by load balancer (e.g. in clouds) or ingress controller.

It may have a form of API - it can be useful for connecting services like Copilot. Using Ingress object, related with specific IngressController, may help in restricting the access to the API. This case is especially useful when developing application, that is enriched by ai-based generation.

Another way is to deploy client-side application like [text-generation-webui](https://github.com/oobabooga/text-generation-webui), where users can interact with web app like with normal ai-powered chat. In order to do this, new Deployment (Argo App/Rollout) must be created, and service properly exposed via Ingress. Then, the API may be hidden inside the cluster (ClusterIP). If some endpoints of the API should be exposed outside, it can be done via proper Ingress configuration.