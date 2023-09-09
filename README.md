# IGUS_Delta_Robot
A Library to control the movement for the Delta Robot from IGUS and the opening and orientation of the Gripper
## TODO
- [ ] read_error:                    coils 20-30
- [ ] read_error_kinematics:         coils 37-44
- [x] shutdown:                      coil 51
- [x] reset:                         coil 52 
  
- [x] move_axes:                     coil 103, coil 104(relative)
- [x] enable_zero_torque:            coil 111
- [ ] is_program_loaded:             coil 120

- [ ] directories                    coils 130-136 

- [x] write_global_signal            coils 200-299 
- [x] write_digital_output           coils 300-363 
- [x] read_digital_input             coils 364-427 
  
  
- [ ] errors                         input_registers 25-43
- [ ] get_kinematics_error_code      input_register 95                    enum
- [ ] get_operation_mode_code        input_register 96                    enum

- [x] get_cartesian_orientation      input_registers 136-141 
- [ ] get_axes_position              input_registers 142-153

- [ ] read_count_programs            input_register 262
- [ ] read_program_number            input_register 263
- [ ] get_why_stopped                input_register 266                   enum 

- [ ] directories                    input_registers 331-396 

- [ ] read_digital_input             input_registers 207-210
- [ ] read_short_message             input_registers 400-431              string
- [ ] get_number_variables           input_registers 440-455
- [ ] get_position_variables
  
  
- [x] set_orientation_endeffector    holding_registers 136-141 
- [x] set_position_axes              holding_registers 142-153 
- [ ] set_override_velocity          holding_registers 181-186

- [ ] run_state                      holding_register 260                 enum
- [ ] replay_mode                    holding_register 261                 enum
  
- [x] set_program_name               holding_registers 267-298            string
- [ ] number_selected_directory      holding_register 332
  
- [ ] set_global_signals             holding_registers 200-206
- [ ] set_digital outputs            holding_registers 207-210
  
- [ ] set_number_variables           holding_registers 440-455
- [ ] set_position_variables         holding_registers 456-711
