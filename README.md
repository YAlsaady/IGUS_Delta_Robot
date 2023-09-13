# IGUS_Delta_Robot
A Library to control the movement for the Delta Robot from IGUS and the opening and orientation of the Gripper
## TODO
- [x] read_error:                    coils 20-30
- [x] read_error_kinematics:         coils 37-44

- [x] shutdown:                      coil 51
- [x] reset:                         coil 52 
  
- [x] move_axes:                     coil 103, coil 104(relative)
- [x] enable_zero_torque:            coil 111
- [x] is_program_loaded:             coil 120

- [ ] directories                    coils 130-136 

- [x] write_global_signal            coils 200-299 
- [x] write_digital_output           coils 300-363 
- [x] read_digital_input             coils 364-427 
  
  
- [x] errors                         input_registers 25-43
- [x] get_kinematics_error_code      input_register 95                    enum
- [x] get_operation_mode_code        input_register 96                    enum

- [x] get_cartesian_orientation      input_registers 136-141 
- [x] get_axes_position              input_registers 142-153

- [x] read_count_programs            input_register 262
- [x] read_program_number            input_register 263
- [x] get_why_stopped                input_register 266                   enum 

- [ ] directories                    input_registers 331-396 

- [ ] read_digital_input             input_registers 207-210
- [x] get_error_message_short        input_registers 400-431              string

- [x] get_number_variables           input_registers 440-455
- [x] get_position_variables         input_registers 456-711
  
  
- [x] set_orientation_endeffector    holding_registers 136-141 
- [x] set_position_axes              holding_registers 142-153 
- [ ] set_override_velocity          holding_registers 187?

- [x] run_state                      holding_register 260                 enum
- [x] replay_mode                    holding_register 261                 enum
  
- [x] set_program_name               holding_registers 267-298            string
- [ ] number_selected_directory      holding_register 332
  
- [x] set_global_signals             holding_registers 200-206
- [x] set_digital outputs            holding_registers 207-210
  
- [x] set_number_variables           holding_registers 440-455
- [x] set_position_variables         holding_registers 456-711
