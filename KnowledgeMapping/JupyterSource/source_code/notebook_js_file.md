    /**
     * Contains and manages cells.
     * @class Notebook
     * @param {string}          selector
     * @param {object}          options - Dictionary of keyword arguments.  
     * @param {jQuery}          options.events - selector of Events
     * @param {KeyboardManager} options.keyboard_manager
     * @param {Contents}        options.contents
     * @param {SaveWidget}      options.save_widget
     * @param {object}          options.config
     * @param {string}          options.base_url
     * @param {string}          options.notebook_path
     * @param {string}          options.notebook_name
     */



Notebook.prototype.validate_config = function()


Notebook.prototype.create_elements = function ()


Notebook.prototype.bind_events = function ()
Notebook.prototype.show_command_palette = function()
显示命令调色板


Notebook.prototype.show_shortcuts_editor = function()
Notebook.prototype.warn_nbformat_minor = function ()


Notebook.prototype.set_dirty = function (value)
设置脏标签，触发set_dirty.Notebook事件

Notebook.prototype.scroll_to_cell = function (index, time)
滚到指定cell的顶部（百分之0的位置）

Notebook.prototype.scroll_cell_percent = function (index, percent, time)
滚动百分比

Notebook.prototype.scroll_to_bottom = function ()
滚动

Notebook.prototype.scroll_to_top = function ()
滚动

Notebook.prototype.edit_metadata = function ()
显示一个模态框询问是否允许用户编辑元数据

Notebook.prototype.get_cell_elements = function ()
返回一个所有cell元素的选择器

Notebook.prototype.get_cell_element = function (index)
获取特定的单元格元素

Notebook.prototype.get_msg_cell = function (msg_id)
获得特定单元格的msg_id

Notebook.prototype.ncells = function ()
返回cell数量

Notebook.prototype.get_cells = function ()
获取所有cell对象

Notebook.prototype.get_cell = function (index)
获得指定index的cell对象

Notebook.prototype.get_next_cell = function (cell)
返回下一个cell

Notebook.prototype.toggle_all_line_numbers = function ()
切换单元格的行号显示

Notebook.prototype.get_prev_cell = function (cell)
获得上一个cell

Notebook.prototype.find_cell_index = function (cell)
获得cell的index

Notebook.prototype.index_or_selected = function (index)
如果已定义，则返回给定的索引，否则返回选定的索引。

Notebook.prototype.get_selected_cells = function ()
返回被选中的所有cell，用于merge

Notebook.prototype.get_selected_cells_indices = function ()
返回被选中的所有cell索引的数组

Notebook.prototype.get_selected_cell = function ()
获得备选的cell

Notebook.prototype.is_valid_cell_index = function (index)
检查cell的index

Notebook.prototype.get_anchor_index = function ()
返回选择当前锚定的单元格的索引，用于move

Notebook.prototype.get_selected_index = function ()
返回被选状态cell的index

Notebook.prototype.extend_selection_by = function(delta)


Notebook.prototype.update_soft_selection = function(){


Notebook.prototype._contract_selection = function(){
锚点移动到selected状态的cell

Notebook.prototype.select = function (index, moveanchor)


Notebook.prototype.select_next = function (moveanchor)


Notebook.prototype.select_prev = function (moveanchor)


Notebook.prototype.get_edit_index = function ()
获取处于编辑模式的cell


Notebook.prototype.handle_command_mode = function (cell)
当cell处于blurs()失去焦点时，进入命令模式


Notebook.prototype.command_mode = function ()
进入命令模式

Notebook.prototype.handle_edit_mode = function (cell)
单元格触发edit_mode事件时处理

Notebook.prototype.edit_mode = function ()
进入编辑模式

Notebook.prototype.ensure_focused = function()
确保cell和codemirror处于激活状态

Notebook.prototype.focus_cell = function ()
激活现有备选的cell

Notebook.prototype.move_cell_up = function (index)


Notebook.prototype.move_cell_down = function (index)


Notebook.prototype._unsafe_delete_cell = function (index)


Notebook.prototype.delete_cells = function(indices)


Notebook.prototype.delete_cell = function (index)


Notebook.prototype.undelete_cell = function()


Notebook.prototype.insert_cell_above = function (type, index)


Notebook.prototype.insert_cell_below = function (type, index)


Notebook.prototype.cells_to_code = function (indices)


Notebook.prototype.to_code = function (index)


Notebook.prototype.cells_to_markdown = function (indices)


Notebook.prototype.to_markdown = function (index)


Notebook.prototype.cells_to_raw = function (indices)


Notebook.prototype.to_raw = function (index)


Notebook.prototype._warn_heading = function ()


Notebook.prototype.to_heading = function (index, level)


Notebook.prototype.enable_paste = function ()


Notebook.prototype.disable_paste = function ()


Notebook.prototype.cut_cell = function ()


Notebook.prototype.copy_cell = function ()


Notebook.prototype.paste_cell_replace = function ()


Notebook.prototype.paste_cell_above = function ()


Notebook.prototype.paste_cell_below = function ()


Notebook.prototype.render_cell_output = function (code_cell)


Notebook.prototype.split_cell = function ()


Notebook.prototype.merge_cells = function(indices, into_last)


Notebook.prototype.merge_selected_cells = function()


Notebook.prototype.merge_cell_above = function ()


Notebook.prototype.merge_cell_below = function ()


Notebook.prototype.insert_image = function ()


Notebook.prototype.cut_cell_attachments = function()


Notebook.prototype.copy_cell_attachments = function()


Notebook.prototype.paste_cell_attachments = function()


Notebook.prototype.disable_attachments_paste = function ()


Notebook.prototype.enable_attachments_paste = function ()


Notebook.prototype.set_insert_image_enabled = function(enabled)


Notebook.prototype.collapse_output = function (index)


Notebook.prototype.collapse_all_output = function ()


Notebook.prototype.expand_output = function (index)


Notebook.prototype.expand_all_output = function ()


Notebook.prototype.clear_output = function (index)


Notebook.prototype.clear_cells_outputs = function(indices)


Notebook.prototype.clear_all_output = function ()


Notebook.prototype.scroll_output = function (index)


Notebook.prototype.scroll_all_output = function ()


Notebook.prototype.toggle_output = function (index)


Notebook.prototype.toggle_cells_outputs = function(indices)


Notebook.prototype.toggle_all_output = function ()


Notebook.prototype.toggle_output_scroll = function (index)


Notebook.prototype.toggle_cells_outputs_scroll = function(indices)


Notebook.prototype.toggle_all_output_scroll = function ()


Notebook.prototype.cell_toggle_line_numbers = function()


Notebook.prototype.start_session = function (kernel_name)


Notebook.prototype.restart_run_all = function (options)


Notebook.prototype.restart_clear_output = function (options)


Notebook.prototype.shutdown_kernel = function (options)


Notebook.prototype.restart_kernel = function (options)


Notebook.prototype._restart_kernel = function (options)


Notebook.prototype.close_and_halt = function ()


Notebook.prototype.execute_cells = function (indices)


Notebook.prototype.execute_selected_cells = function ()


Notebook.prototype.execute_cell = function ()


Notebook.prototype.execute_cell_and_insert_below = function ()


Notebook.prototype.execute_cell_and_select_below = function ()


Notebook.prototype.execute_cells_below = function ()


Notebook.prototype.execute_cells_above = function ()


Notebook.prototype.execute_all_cells = function ()


Notebook.prototype.execute_cell_range = function (start, end)


Notebook.prototype.get_notebook_name = function ()


Notebook.prototype.set_notebook_name = function (name)


Notebook.prototype.test_notebook_name = function (nbname)


Notebook.prototype.fromJSON = function (data)


Notebook.prototype.toJSON = function ()


Notebook.prototype.set_autosave_interval = function (interval)


Notebook.prototype.save_notebook = function (check_last_modified)


Notebook.prototype.save_notebook_success = function (start, data)


Notebook.prototype._update_autosave_interval = function (start)


Notebook.prototype.trust_notebook = function ()


Notebook.prototype.copy_notebook = function ()


Notebook.prototype.ensure_extension = function (name)


Notebook.prototype.rename = function (new_name)


Notebook.prototype.delete = function ()


Notebook.prototype.load_notebook = function (notebook_path)


Notebook.prototype.load_notebook_success = function (data)


Notebook.prototype.load_notebook_error = function (error)


Notebook.prototype.save_checkpoint = function ()


Notebook.prototype.add_checkpoint = function (checkpoint)


Notebook.prototype.list_checkpoints = function ()


Notebook.prototype.list_checkpoints_success = function (data)


Notebook.prototype.create_checkpoint = function ()


Notebook.prototype.create_checkpoint_success = function (data)


Notebook.prototype.restore_checkpoint_dialog = function (checkpoint)


Notebook.prototype.restore_checkpoint = function (checkpoint)


Notebook.prototype.restore_checkpoint_success = function ()


Notebook.prototype.delete_checkpoint = function (checkpoint)


Notebook.prototype.delete_checkpoint_success = function ()

