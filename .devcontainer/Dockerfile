# bring in the micromamba image so we can copy files from it
FROM mambaorg/micromamba:1.5.6
ARG MAMBA_USER=$user
USER root
# The folder to use as a workspace. The project should be mounted here.
ARG DEV_WORK_DIR=/workspace

COPY .devcontainer/scripts/common-debian-patched.sh /tmp/
RUN bash /tmp/common-debian-patched.sh true $MAMBA_USER && rm /tmp/common-debian-patched.sh


COPY .devcontainer/features/install.sh /tmp/install.sh
RUN DOCKERDASHCOMPOSEVERSION=v2 bash /tmp/install.sh && rm /tmp/install.sh

# Make sure everyone can access the working directory.
ARG DEV_WORK_DIR
RUN : \
    && mkdir --parents --mode=777 "${DEV_WORK_DIR}" \
    && chown "$MAMBA_USER:$MAMBA_USER" "${DEV_WORK_DIR}"

USER $MAMBA_USER

ARG ENVYML=/tmp/env.yml
# The folder to use as a workspace. The project should be mounted here.
COPY --chown=$MAMBA_USER:$MAMBA_USER .devcontainer/env.yml  /tmp/env.yml
# Extract the environment name from the env.yaml file
RUN ENV_NAME=$(grep 'name:' $ENVYML | awk '{print $2}') && \
    echo "Environment Name: $ENV_NAME"

RUN micromamba create -f /tmp/env.yml && \
    micromamba clean --all --yes && \
    chmod -R 777 /opt/conda
# Activate the conda environment for the Dockerfile.
# <https://github.com/mamba-org/micromamba-docker#running-commands-in-dockerfile-within-the-conda-environment>
ARG MAMBA_DOCKERFILE_ACTIVATE=1

# Set CMD script to run on container startup.
COPY .devcontainer/features/_dev-init.sh /usr/local/bin/_dev-init.sh
COPY .devcontainer/features/_configure-docker-group.sh /usr/local/bin/_configure-docker-group.sh


# Script which launches commands passed to "docker run"
COPY .devcontainer/features/_entrypoint.sh /usr/local/bin/_entrypoint.sh
COPY .devcontainer/features/_activate_current_env.sh /usr/local/bin/_activate_current_env.sh
ENTRYPOINT ["/usr/local/bin/_entrypoint.sh"]

# Default command for "docker run"
CMD ["/bin/bash"]

