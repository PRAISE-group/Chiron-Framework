define i32 @main() {
entry:
  %":y" = alloca i32, align 4
  %":x" = alloca i32, align 4
  store i32 5, ptr %":x", align 4
  store i32 5, ptr %":y", align 4
  %":x1" = load i32, ptr %":x", align 4
  %":y2" = load i32, ptr %":y", align 4
  %lttmp = icmp slt i32 %":x1", %":y2"
  br i1 %lttmp, label %then, label %else

then:                                             ; preds = %entry
  %":x3" = load i32, ptr %":x", align 4
  %addtmp = add i32 %":x3", 1
  store i32 %addtmp, ptr %":x", align 4
  br label %ifcont

else:                                             ; preds = %entry
  %":x4" = load i32, ptr %":x", align 4
  %addtmp5 = add i32 %":x4", 2
  store i32 %addtmp5, ptr %":x", align 4
  br label %ifcont

ifcont:                                           ; preds = %else, %then
  ret i32 0
}
