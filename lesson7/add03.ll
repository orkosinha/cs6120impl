; ModuleID = 'tests/add03.cpp'
source_filename = "tests/add03.cpp"
target datalayout = "e-m:e-i8:8:32-i16:16:32-i64:64-i128:128-n32:64-S128"
target triple = "aarch64-unknown-linux-gnu"

@.str = private unnamed_addr constant [10 x i8] c"Sum = %d\0A\00", align 1

; Function Attrs: noinline norecurse optnone
define dso_local i32 @main() #0 {
  %1 = alloca i32, align 4
  %2 = alloca i32, align 4
  %3 = alloca i32, align 4
  %4 = alloca i32, align 4
  %5 = alloca i32, align 4
  %6 = alloca i32, align 4
  %7 = alloca i32, align 4
  %8 = alloca i32, align 4
  %9 = alloca i32, align 4
  %10 = alloca i32, align 4
  %11 = alloca i32, align 4
  %12 = alloca i32, align 4
  %13 = alloca i32, align 4
  %14 = alloca i32, align 4
  %15 = alloca i32, align 4
  %16 = alloca i32, align 4
  %17 = alloca i32, align 4
  %18 = alloca i32, align 4
  %19 = alloca i32, align 4
  %20 = alloca i32, align 4
  %21 = alloca i32, align 4
  %22 = alloca i32, align 4
  %23 = alloca i32, align 4
  %24 = alloca i32, align 4
  %25 = alloca i32, align 4
  %26 = alloca i32, align 4
  %27 = alloca i32, align 4
  store i32 0, i32* %1, align 4
  store i32 2, i32* %2, align 4
  %28 = load i32, i32* %2, align 4
  %29 = load i32, i32* %2, align 4
  %30 = add nsw i32 %28, %29
  store i32 %30, i32* %3, align 4
  %31 = load i32, i32* %3, align 4
  %32 = load i32, i32* %3, align 4
  %33 = add nsw i32 %31, %32
  store i32 %33, i32* %4, align 4
  %34 = load i32, i32* %4, align 4
  %35 = load i32, i32* %4, align 4
  %36 = add nsw i32 %34, %35
  store i32 %36, i32* %5, align 4
  %37 = load i32, i32* %5, align 4
  %38 = load i32, i32* %5, align 4
  %39 = add nsw i32 %37, %38
  store i32 %39, i32* %6, align 4
  %40 = load i32, i32* %6, align 4
  %41 = load i32, i32* %6, align 4
  %42 = add nsw i32 %40, %41
  store i32 %42, i32* %7, align 4
  %43 = load i32, i32* %7, align 4
  %44 = load i32, i32* %7, align 4
  %45 = add nsw i32 %43, %44
  store i32 %45, i32* %8, align 4
  %46 = load i32, i32* %8, align 4
  %47 = load i32, i32* %8, align 4
  %48 = add nsw i32 %46, %47
  store i32 %48, i32* %9, align 4
  %49 = load i32, i32* %9, align 4
  %50 = load i32, i32* %9, align 4
  %51 = add nsw i32 %49, %50
  store i32 %51, i32* %10, align 4
  %52 = load i32, i32* %10, align 4
  %53 = load i32, i32* %10, align 4
  %54 = add nsw i32 %52, %53
  store i32 %54, i32* %11, align 4
  %55 = load i32, i32* %11, align 4
  %56 = load i32, i32* %11, align 4
  %57 = add nsw i32 %55, %56
  store i32 %57, i32* %12, align 4
  %58 = load i32, i32* %12, align 4
  %59 = load i32, i32* %12, align 4
  %60 = add nsw i32 %58, %59
  store i32 %60, i32* %13, align 4
  %61 = load i32, i32* %13, align 4
  %62 = load i32, i32* %13, align 4
  %63 = add nsw i32 %61, %62
  store i32 %63, i32* %14, align 4
  %64 = load i32, i32* %14, align 4
  %65 = load i32, i32* %14, align 4
  %66 = add nsw i32 %64, %65
  store i32 %66, i32* %15, align 4
  %67 = load i32, i32* %15, align 4
  %68 = load i32, i32* %15, align 4
  %69 = add nsw i32 %67, %68
  store i32 %69, i32* %16, align 4
  %70 = load i32, i32* %16, align 4
  %71 = load i32, i32* %16, align 4
  %72 = add nsw i32 %70, %71
  store i32 %72, i32* %17, align 4
  %73 = load i32, i32* %17, align 4
  %74 = load i32, i32* %17, align 4
  %75 = add nsw i32 %73, %74
  store i32 %75, i32* %18, align 4
  %76 = load i32, i32* %18, align 4
  %77 = load i32, i32* %18, align 4
  %78 = add nsw i32 %76, %77
  store i32 %78, i32* %19, align 4
  %79 = load i32, i32* %19, align 4
  %80 = load i32, i32* %19, align 4
  %81 = add nsw i32 %79, %80
  store i32 %81, i32* %20, align 4
  %82 = load i32, i32* %20, align 4
  %83 = load i32, i32* %20, align 4
  %84 = add nsw i32 %82, %83
  store i32 %84, i32* %21, align 4
  %85 = load i32, i32* %21, align 4
  %86 = load i32, i32* %21, align 4
  %87 = add nsw i32 %85, %86
  store i32 %87, i32* %22, align 4
  %88 = load i32, i32* %22, align 4
  %89 = load i32, i32* %22, align 4
  %90 = add nsw i32 %88, %89
  store i32 %90, i32* %23, align 4
  %91 = load i32, i32* %23, align 4
  %92 = load i32, i32* %23, align 4
  %93 = add nsw i32 %91, %92
  store i32 %93, i32* %24, align 4
  %94 = load i32, i32* %24, align 4
  %95 = load i32, i32* %24, align 4
  %96 = add nsw i32 %94, %95
  store i32 %96, i32* %25, align 4
  %97 = load i32, i32* %25, align 4
  %98 = load i32, i32* %25, align 4
  %99 = add nsw i32 %97, %98
  store i32 %99, i32* %26, align 4
  %100 = load i32, i32* %26, align 4
  %101 = load i32, i32* %26, align 4
  %102 = add nsw i32 %100, %101
  store i32 %102, i32* %27, align 4
  %103 = load i32, i32* %27, align 4
  %104 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([10 x i8], [10 x i8]* @.str, i64 0, i64 0), i32 %103)
  ret i32 0
}

declare dso_local i32 @printf(i8*, ...) #1

attributes #0 = { noinline norecurse optnone "correctly-rounded-divide-sqrt-fp-math"="false" "disable-tail-calls"="false" "frame-pointer"="non-leaf" "less-precise-fpmad"="false" "min-legal-vector-width"="0" "no-infs-fp-math"="false" "no-jump-tables"="false" "no-nans-fp-math"="false" "no-signed-zeros-fp-math"="false" "no-trapping-math"="true" "stack-protector-buffer-size"="8" "target-cpu"="generic" "target-features"="+neon" "unsafe-fp-math"="false" "use-soft-float"="false" }
attributes #1 = { "correctly-rounded-divide-sqrt-fp-math"="false" "disable-tail-calls"="false" "frame-pointer"="non-leaf" "less-precise-fpmad"="false" "no-infs-fp-math"="false" "no-nans-fp-math"="false" "no-signed-zeros-fp-math"="false" "no-trapping-math"="true" "stack-protector-buffer-size"="8" "target-cpu"="generic" "target-features"="+neon" "unsafe-fp-math"="false" "use-soft-float"="false" }

!llvm.module.flags = !{!0}
!llvm.ident = !{!1}

!0 = !{i32 1, !"wchar_size", i32 4}
!1 = !{!"Debian clang version 11.0.1-2"}
