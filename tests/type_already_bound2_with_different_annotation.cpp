// expect-success
/*
 * Copyright 2014 Google Inc. All rights reserved.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 * 
 *     http://www.apache.org/licenses/LICENSE-2.0
 * 
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

#include <fruit/fruit.h>

using fruit::Component;
using fruit::Injector;
using fruit::createComponent;

struct Annotation1 {};
struct Annotation2 {};

using intAnnot1 = fruit::Annotated<Annotation1, int>;
using intAnnot2 = fruit::Annotated<Annotation2, int>;

Component<intAnnot1> getParentComponent() {
  return createComponent()
    .registerConstructor<intAnnot1()>();
}

Component<intAnnot1, intAnnot2> getComponent() {
  return createComponent()
    .registerConstructor<intAnnot2()>()
    .install(getParentComponent());
}

int main() {
  fruit::Injector<intAnnot1, intAnnot2> injector(getComponent());
  int& n1 = injector.get<fruit::Annotated<Annotation1, int&>>();
  int& n2 = injector.get<fruit::Annotated<Annotation2, int&>>();
  assert(&n1 != &n2);
  return 0;
}
