#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "GitWorkshopHello.generated.h"

UCLASS()
class UEGITWORKSHOP_API AGitWorkshopHello : public AActor
{
    GENERATED_BODY()

public:
    AGitWorkshopHello();
    virtual void BeginPlay() override;
};
