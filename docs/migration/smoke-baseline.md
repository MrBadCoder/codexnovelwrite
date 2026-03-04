usage: webnovel.py [-h] [--project-root PROJECT_ROOT]
                   {where,use,index,state,rag,style,entity,context,migrate,workflow,status,update-state,backup,archive,init,extract-context} ...

webnovel unified CLI

positional arguments:
  {where,use,index,state,rag,style,entity,context,migrate,workflow,status,update-state,backup,archive,init,extract-context}
    where               打印解析出的 project_root
    use                 绑定当前工作区使用的书项目（写入指针/registry）
    index               转发到 index_manager
    state               转发到 state_manager
    rag                 转发到 rag_adapter
    style               转发到 style_sampler
    entity              转发到 entity_linker
    context             转发到 context_manager
    migrate             转发到 migrate_state_to_sqlite
    workflow            转发到 workflow_manager.py
    status              转发到 status_reporter.py
    update-state        转发到 update_state.py
    backup              转发到 backup_manager.py
    archive             转发到 archive_manager.py
    init                转发到 init_project.py（初始化项目）
    extract-context     转发到 extract_chapter_context.py

options:
  -h, --help            show this help message and exit
  --project-root PROJECT_ROOT
                        书项目根目录或工作区根目录（可选，默认自动检测）
